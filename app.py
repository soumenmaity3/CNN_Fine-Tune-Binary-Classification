import streamlit as st
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import numpy as np
from PIL import Image

# Set page config
st.set_page_config(
    page_title="Cat vs Dog Classifier",
    page_icon="🐾",
    layout="centered"
)

# Constants
MODEL_PATH = 'models/model.h5'
IMAGE_SIZE = (150, 150)
CLASSES = ['Cat', 'Dog']

@st.cache_resource
def load_classifier_model():
    """Load the trained model from disk."""
    try:
        model = load_model(MODEL_PATH)
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

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

def main():
    st.title("🐱 Cat vs Dog Classifier 🐶")
    st.markdown("Upload an image to see if it's a **Cat** or a **Dog**!")

    # Load model
    with st.spinner("Loading model..."):
        model = load_classifier_model()

    if model is None:
        st.warning("Model could not be loaded. Please check if 'models/model.h5' exists.")
        return

    # File uploader
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "webp"])

    if uploaded_file is not None:
        try:
            # Display image
            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded Image', use_column_width=True)
            
            # Predict button
            if st.button('Predict'):
                with st.spinner('Analyzing...'):
                    # Preprocess
                    processed_image = preprocess_image(image)
                    
                    # Predict
                    prediction = model.predict(processed_image)
                    
                    # Output is binary: < 0.5 is Class 0 (Cat), > 0.5 is Class 1 (Dog)
                    # Based on standard flow_from_directory alphabetical order
                    # Cat comes before Dog, so 0=Cat, 1=Dog.
                    
                    score = prediction[0][0]
                    print(f'The Prediction score is: {score}')
                    predicted_class = CLASSES[1] if score > 0.5 else CLASSES[0]
                    confidence = score if score > 0.5 else 1 - score
                    
                    # Display result
                    st.success(f"Prediction: **{predicted_class}**")
                    st.info(f"Confidence: {confidence:.2%}")
                    
                    # Optional: Progress bar for confidence
                    # st.progress(int(confidence * 100))
                    
        except Exception as e:
            st.error(f"Error processing image: {e}")

if __name__ == "__main__":
    main()
