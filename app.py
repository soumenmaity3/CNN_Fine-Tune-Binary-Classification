import os
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from flask import Flask, request, jsonify
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Constants
MODEL_PATH = 'models/model.h5'
IMAGE_SIZE = (150, 150)
CLASSES = ['Cat', 'Dog']

# Global model variable
model = None

def load_classifier_model():
    """Load the trained model from disk."""
    global model
    try:
        model = load_model(MODEL_PATH)
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Error loading model: {e}")
        model = None

def preprocess_image(image):
    """
    Preprocess the image to match model requirements:
    1. Resize to (150, 150)
    2. Convert to array
    3. Expand dimensions (batch size 1)
    4. Apply MobileNetV2 preprocessing
    """
    # Resize
    if image.mode != "RGB":
        image = image.convert("RGB")
    
    image = image.resize(IMAGE_SIZE)
    
    # Convert to array
    img_array = img_to_array(image)
    
    # Expand dims to make it (1, 150, 150, 3)
    img_array = np.expand_dims(img_array, axis=0)
    
    # Preprocess
    img_processed = preprocess_input(img_array)
    
    return img_processed

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500

    try:
        image = Image.open(file.stream)
        processed_image = preprocess_image(image)
        
        prediction = model.predict(processed_image)
        
        # Output is binary: < 0.5 is Class 0 (Cat), > 0.5 is Class 1 (Dog)
        score = float(prediction[0][0])
        predicted_class = CLASSES[1] if score > 0.5 else CLASSES[0]
        confidence = score if score > 0.5 else 1 - score
        
        return jsonify({
            'class': predicted_class,
            'confidence': float(confidence),
            'score': score
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Load model on startup
    load_classifier_model()
    # Run app
    app.run(debug=True, host='0.0.0.0', port=5000)
