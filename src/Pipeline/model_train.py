import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.Component.data_ingestion import DataGenerator
from src.logger import logging
from src.Pipeline.fine_tune_model import MobileNetV2Model
from src.Exception import CustomException as cuexc

class ModelTrain:
    def __init__(self):
        self.model_builder = MobileNetV2Model()
        self.model = self.model_builder.model
        self.data_generator = DataGenerator()
    
    def initiate_model_training(self):
        try:
            logging.info("Model Training Started")
            train_gen, val_gen, test_gen = self.data_generator.data_generator()
            
            logging.info(f"Training with {train_gen.samples} samples, validating with {val_gen.samples} samples")

            history = self.model.fit(
                train_gen,
                epochs=10,
                validation_data=val_gen,
                validation_steps=val_gen.samples // val_gen.batch_size,
                steps_per_epoch=train_gen.samples // train_gen.batch_size
            )
            
            # Save the model
            model_path = project_root / 'models' / 'model.h5'
            model_path.parent.mkdir(parents=True, exist_ok=True)
            self.model.save(str(model_path))
            logging.info(f"Model saved at {model_path}")
            
            return history
            
        except Exception as e:
            logging.error(f"Error in model training: {e}")
            raise cuexc(e, sys)

if __name__ == "__main__":
    try:
        trainer = ModelTrain()
        trainer.initiate_model_training()
    except Exception as e:
        print(f"Training failed: {e}")