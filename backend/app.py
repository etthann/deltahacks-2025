from flask import Flask, jsonify,request
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a file handler
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.INFO)

# Create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

@app.route('/')
def home():
    return jsonify({'message': 'Welcome to SignLanguageAI'})


if __name__ == "__main__":
    app.run(debug=True, port=5000)