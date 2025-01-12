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

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Load environment variables
load_dotenv()

# MongoDB Atlas connection string from .env file
app.config["MONGO_URI"] = os.getenv("MONGO_URI")

client = MongoClient(app.config["MONGO_URI"])
db = client.get_database('skin_disease')  # Replace with your database name
collection = db.get_collection('user_skin_disease')  # Replace with your collection name

# Configure the logger
def setup_logger():
    logger = logging.getLogger('SkinDiseasePrediction')
    logger.setLevel(logging.DEBUG)

    # Create a file handler for writing logs to a file
    file_handler = RotatingFileHandler('app.log', maxBytes=5*1024*1024, backupCount=3)
    file_handler.setLevel(logging.DEBUG)

    # Create a console handler for outputting logs to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Define a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Initialize the logger
logger = setup_logger()

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

def dummy_ai_process(img):
    # Placeholder for your AI model processing
    logger.debug("dummy_ai_process called")
    return "AI processed result"

if __name__ == '__main__':
    logger.info("Starting Flask app")
    app.run(debug=True, port=5000)
