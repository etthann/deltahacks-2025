from flask import Flask, jsonify, request, session
from flask_cors import CORS
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import base64
import pickle
import numpy as np
from PIL import Image
import io
from authentication import Authentication

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key')

# Configure MongoDB client with SSL
MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=True)

# Specify the database name
db_name = os.getenv('DB_NAME', 'test')
db = client[db_name]
users = db.users

@app.route("/")
def index():
    return jsonify({'message': 'Hello World'}) , 200

@app.route('/register', methods=['POST'])
def register():
    return Authentication.register_user(users)

@app.route('/login', methods=['POST'])
def login():
    return Authentication.login_user(users)

@app.route('/upload', methods=['POST'])
def upload():
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'User not logged in'}), 401

        user_id = session['user_id']
        data = request.get_json()
        image_data = data['image']
        # Decode the base64 string
        image_bytes = base64.b64decode(image_data.split(',')[1])

        # Load the model from the pickle file
        pickle_file_path = 'backend/model/model.pkl'
        with open(pickle_file_path, 'rb') as file:
            model = pickle.load(file)

        # Preprocess the image
        image = Image.open(io.BytesIO(image_bytes))
        image = image.resize((180, 180))  # Resize to the expected input size
        image_array = np.array(image) / 255.0  # Normalize the image
        image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension

        # Feed the image to the model
        predictions = model.predict(image_array)

        # Create an entry for the image and its results
        image_entry = {
            'image': image_data,
            'results' : 'testing',
        }

        # Store the image and results in the user's document
        users.update_one(
            {'_id': user_id},
            {'$push': {'images': image_entry}}
        )

        return jsonify({'message': 'Image uploaded and processed successfully', 'Data': predictions }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/check_login', methods=['GET'])
def check_login():
    if 'user_id' in session:
        return jsonify({'logged_in': True}), 200
    else:
        return jsonify({'logged_in': False}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)