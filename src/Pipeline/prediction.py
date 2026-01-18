import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tensorflow.keras.models import load_model
from sklearn.metrics import confusion_matrix, classification_report
from src.Component.data_ingestion import DataGenerator
from src.logger import logging
from src.Exception import CustomException as cuexc

class PredictionPipeline:
    def __init__(self):
        self.model_path = project_root / 'models' / 'model.h5'
        # self.test_data_path = project_root / 'data' / 'processed' / 'cat-dog-split' / 'test'
        self.confusion_matrix_path = project_root / 'confusion_matrix.png'

    def run(self):
        try:
            logging.info("Prediction Pipeline Started")
            
            # Load Model
            if not self.model_path.exists():
                raise FileNotFoundError(f"Model not found at {self.model_path}")
            
            logging.info(f"Loading model from {self.model_path}")
            model = load_model(str(self.model_path))
            
            # Data Generator for Test Data
            _,_,test_generator = DataGenerator().data_generator()
            

            
            # Make Predictions
            logging.info("Generating predictions...")
            predictions = model.predict(test_generator)
            predicted_classes = (predictions > 0.5).astype(int).flatten()
            true_classes = test_generator.classes
            class_labels = list(test_generator.class_indices.keys())
            
            # Confusion Matrix
            logging.info("Computing confusion matrix...")
            cm = confusion_matrix(true_classes, predicted_classes)
            
            # Plotting
            plt.figure(figsize=(10, 8))
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=class_labels, yticklabels=class_labels)
            plt.title('Confusion Matrix')
            plt.ylabel('True Label')
            plt.xlabel('Predicted Label')
            plt.tight_layout()
            
            # Save Plot
            plt.savefig(str(self.confusion_matrix_path))
            logging.info(f"Confusion matrix saved at {self.confusion_matrix_path}")
            print(f"Confusion matrix saved at {self.confusion_matrix_path}")
            
            # Classification Report
            report = classification_report(true_classes, predicted_classes, target_names=class_labels)
            logging.info(f"Classification Report:\n{report}")
            print("Classification Report:")
            print(report)
            
        except Exception as e:
            logging.error(f"Error in prediction pipeline: {e}")
            raise cuexc(e, sys)

if __name__ == "__main__":
    try:
        pipeline = PredictionPipeline()
        pipeline.run()
    except Exception as e:
        print(f"Prediction failed: {e}")
