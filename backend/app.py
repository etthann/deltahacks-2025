from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import io
from PIL import Image
import logging
from logging.handlers import RotatingFileHandler
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import bcrypt
import re

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Load environment variables
load_dotenv()

# MongoDB Atlas connection string from .env file
app.config["MONGO_URI"] = os.getenv("MONGO_URI")

client = MongoClient(app.config["MONGO_URI"])
db = client.get_database('skin_disease')  # Replace with your database name
collection = db.get_collection('user_skin_disease')  # Replace with your collection name
users_collection = db.get_collection('users')  # Collection to store user info


# Configure the logger
def setup_logger():
    logger = logging.getLogger('SkinDiseasePrediction')
    logger.setLevel(logging.DEBUG)

    # Create a file handler for writing logs to a file
    file_handler = RotatingFileHandler('app.log', maxBytes=5 * 1024 * 1024, backupCount=3)
    file_handler.setLevel(logging.DEBUG)

    # Create a console handler for outputting logs to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Define a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # Corrected here
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# Initialize the logger
logger = setup_logger()


class Authentication:

    @staticmethod
    def register_user(users_collection):
        try:
            data = request.json
            username = data['username']
            password = data['password'].encode('utf-8')
            email = data['email']
            confirm_password = data['confirmPassword'].encode('utf-8')

            # Validate the request data
            validation_message = Authentication.validate_request_data(users_collection, username, password, email,
                                                                      confirm_password)
            if validation_message is not None:
                return validation_message

            # Hash the password
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

            # Store the user with the hashed password
            users_collection.insert_one({
                'username': username,
                'password': hashed_password,
                'email': email
            })

            return jsonify({'message': 'User created successfully'}), 200
        except Exception as e:
            return jsonify({'message': 'An error occurred'}), 500

    @staticmethod
    def validate_request_data(users_collection, username, password, email=None, confirm_password=None):
        username_regex = r'^(?=.*[A-Z])(?=.*[!@#$%^&*(),.?":{}|<>]).*$'
        validations = {
            'Email is required': not email,
            'Username is required': not username,
            'Password is required': not password,
            'Confirm password is required': not confirm_password,
            'Invalid email address': email and not re.match(r"[^@]+@[^@]+\.[^@]+", email),
            'Passwords do not match': password != confirm_password,
            'Password must be at least 8 characters': password and len(password) < 8,
            'Username must be at least 4 characters': username and len(username) < 4,
            'Username must be alphanumeric, contain an uppercase letter and at least one special character': username and not re.match(
                username_regex, username),
            'Username already exists': username and users_collection.find_one({'username': username}) is not None,
            'Email already exists': email and users_collection.find_one({'email': email}) is not None
        }

        for message, condition in validations.items():
            if condition:
                return jsonify({'message': message}), 400

        return None

    @staticmethod
    def login_user(users_collection):
        data = request.json
        if 'username' not in data or 'password' not in data:
            return jsonify({'message': 'Missing username or password'}), 400

        username = data['username']
        password = data['password'].encode('utf-8')

        if username is None or password is None or username == '' or password == '':
            return jsonify({'message': 'Missing username or password'}), 400

        user = users_collection.find_one({'username': username})
        if user is None:
            return jsonify({'message': 'User does not exist'}), 401

        if not bcrypt.checkpw(password, user['password']):
            return jsonify({'message': 'Invalid password'}), 401

        return jsonify({'message': 'Logged in successfully'}), 200


@app.route('/', methods=['GET'])
def home():
    logger.info("Home route accessed")
    return "Hello World!"


@app.route('/upload', methods=['POST'])
def upload_image():
    data = request.json
    logger.info("Image upload endpoint accessed")

    try:
        # Decode the base64 image
        img_data = base64.b64decode(data['image'])
        img = Image.open(io.BytesIO(img_data))
        logger.debug("Image decoded successfully")

        # Process the image with AI (replace with actual AI call)
        result = dummy_ai_process(img)
        logger.info("AI processing completed")

        # Save file info to MongoDB
        file_info = {
            'filename': data.get('filename', 'unknown'),
            'result': result
        }
        collection.insert_one(file_info)
        logger.info("File info saved to MongoDB")

        if result:
            logger.info("Returning AI result")
            return jsonify({"result": result}), 200
        else:
            logger.warning("AI processing returned no result")
            return jsonify({'result': "Error"}, 400)
    except Exception as e:
        logger.error(f"Error processing image: {e}")
        return jsonify({'result': "Error"}, 400)


@app.route('/login', methods=['POST'])
def login_user():
    return Authentication.login_user(users_collection)


@app.route('/register', methods=['POST'])
def register_user():
    return Authentication.register_user(users_collection)


def dummy_ai_process(img):
    # Placeholder for your AI model processing
    logger.debug("dummy_ai_process called")
    return "AI processed result"


if __name__ == '__main__':
    logger.info("Starting Flask app")
    app.run(debug=True, port=5000)
