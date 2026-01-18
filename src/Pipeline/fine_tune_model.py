import logging,os,sys
from src.logger import logging
from src.Exception import CustomException as cuexc

from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense,Dropout
from tensorflow.keras import Model,Input


class MobileNetV2Model:
    def __init__(self):
        self.model = self.build_model()

    def build_model(self):
        base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(150, 150, 3))

        input = Input(shape=(150, 150, 3))
        x = base_model(input)
        x = GlobalAveragePooling2D()(x)
        x = Dropout(0.2)(x)
        output = Dense(1, activation='sigmoid')(x)

        model = Model(inputs=input, outputs=output)
        
        base_model.trainable = True
        fine_tune_at = len(base_model.layers) - 30
        for layer in base_model.layers[:fine_tune_at]:
            layer.trainable = False
        
        logging.info(f"✅ Total MobileNetV2 layers: {len(base_model.layers)}")
        logging.info(f"🔓 Fine-tuning from layer: {fine_tune_at}")

        
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        logging.info('Model compiletion done..')
        return model