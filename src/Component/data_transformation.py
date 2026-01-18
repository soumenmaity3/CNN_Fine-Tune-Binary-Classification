from src.Component.data_download import DownloadData
from src.Exception import CustomException as cuexc
import os
import logging
from dataclasses import dataclass
import sys,random,shutil
from PIL import Image

class DataTransformation:
    def __init__(self):
        self.download_data = DownloadData()
        self.data_path=self.download_data.run()
    
    def run(self):
        try:
            logging.info("Data Transformation started")
            self.split_data()
            logging.info("Data Transformation completed")
        except Exception as e:
            raise cuexc(e, sys)

    def remove_corrupted_images(self,directory):
        print(f"Checking for corrupted images in: {directory}")
        for root, _, files in os.walk(directory):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    filepath = os.path.join(root, file)
                    try:
                        img = Image.open(filepath)
                        img.verify() # Verify if it's a valid image
                    except (IOError, SyntaxError, Image.UnidentifiedImageError) as e:
                        print(f"Deleting corrupted image: {filepath} ({e})")
                        os.remove(filepath)
    
    def split_data(self):
        try:
            logging.info("Splitting data started")
            source_dir = self.data_path
            output_dir = 'data/processed/cat-dog-split'
            
            #train and test ratio
            train_ratio = 0.8
            test_ratio = 0.2
            
            classes = ['Cat', 'Dog']
            random.seed(42)
            for cls in classes:
                cls_path = os.path.join(source_dir,cls)

                self.remove_corrupted_images(cls_path)

                images = os.listdir(cls_path)
                random.shuffle(images)
                
                train_count = int(len(images)*train_ratio)
                train_images = images[:train_count]
                test_images = images[train_count:]

                train_dir = os.path.join(output_dir,'train',cls)
                test_dir = os.path.join(output_dir,'test',cls)
                os.makedirs(train_dir,exist_ok=True)
                os.makedirs(test_dir,exist_ok=True)

                for img in train_images:
                    shutil.copy(os.path.join(cls_path,img),os.path.join(train_dir,img))
                for img in test_images:
                    shutil.copy(os.path.join(cls_path,img),os.path.join(test_dir,img))

                logging.info(f"{cls} split completed")
                logging.info(f"{cls} split completed")
            logging.info("Data splitting completed")
            
            # Return the parent train and test directories
            # We know the structure is output_dir/train and output_dir/test
            parent_train_dir = os.path.join(output_dir, 'train')
            parent_test_dir = os.path.join(output_dir, 'test')
            
            return parent_train_dir, parent_test_dir
        except Exception as e:
            raise cuexc(e,sys)


# if __name__ == "__main__":
#     data_transformation = DataTransformation()
#     data_transformation.run()
