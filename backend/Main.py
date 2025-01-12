from flask import Flask
from flask_cors import CORS
from flask import request, jsonify
from . import app
import base64
import io
from PIL import Image

app = Flask(__name__)
CORS(app)

@app.route('/',methods=['GET'])
def home():
    return "Hello World!"

@app.route('/upload', methods=['POST'])
def upload_image():
    data = request.json

    # Decode the base64 image
    img_data = base64.b64decode(data['image'])
    img = Image.open(io.BytesIO(img_data))

    # Process the image with AI (replace with actual AI call)
    result = dummy_ai_process(img)

    return jsonify({"result": result}, 200)

def dummy_ai_process(img):
    # Placeholder for your AI model processing
    return "AI processed result"


if __name__ == '__main__':
    app.run(debug=True, port=5000)
