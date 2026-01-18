import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import os
import sys
from PIL import Image
import logging
from src.Component.data_transformation import DataTransformation

class DataGenerator:
    def __init__(self):
        self.data_transformation = DataTransformation()
        self.train_dir,self.test_dir = self.data_transformation.split_data()
        self.TARGET_SIZE = (150,150)
        self.BATCH_SIZE = 32
        self.VALIDATION_SPLIT = 0.2

        self.train_datagen = ImageDataGenerator(
            preprocessing_function = preprocess_input,
            rotation_range = 10,
            zoom_range = 0.2,
            horizontal_flip = True,
            validation_split = self.VALIDATION_SPLIT
        )

    def data_generator(self):
        generator = self.train_datagen
        train_dir = self.train_dir
        test_dir = self.test_dir
        print(train_dir,test_dir)
        train_generat = generator.flow_from_directory(
            train_dir,
            target_size = self.TARGET_SIZE,
            batch_size = self.BATCH_SIZE,
            class_mode = 'binary',
            subset = 'training'
        )
        logging.info("Train Generator is complete")
        validation_generat = generator.flow_from_directory(
            train_dir,
            target_size = self.TARGET_SIZE,
            batch_size = self.BATCH_SIZE,
            class_mode = 'binary',
            subset = 'validation'
        )
        logging.info("Validation Generator is complete")
        test_generator = ImageDataGenerator(preprocessing_function=preprocess_input).flow_from_directory(
            test_dir,
            target_size=self.TARGET_SIZE,
            batch_size=self.BATCH_SIZE,
            class_mode='binary',
            shuffle=False
        )
        logging.info("Test Generator is complete")
        logging.info("Data generators created successfully")
        logging.info(f"Found {train_generat.samples} training images belonging to {train_generat.num_classes} classes.")
        logging.info(f"Found {validation_generat.samples} validation images belonging to {validation_generat.num_classes} classes.")
        logging.info(f"Found {test_generator.samples} testing images belonging to {test_generator.num_classes} classes.")
        
        return train_generat, validation_generat, test_generator

# if __name__ == "__main__":
#     import sys
#     # Add project root to path
#     from pathlib import Path
#     project_root = Path(__file__).parent.parent.parent
#     sys.path.insert(0, str(project_root))
    
#     from src.logger import logging

#     try:
#         gen = DataGenerator()
#         gen.data_generator()
#     except Exception as e:
#         logging.error(f"Failed to run DataGenerator: {e}")
#         raise e