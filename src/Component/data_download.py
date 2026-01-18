import os
import sys
from pathlib import Path

# Add project root to path so imports work correctly
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from kaggle.api.kaggle_api_extended import KaggleApi
import stat
import logging
from src.Exception import CustomException as cuexc


class DownloadData:
    """Class to handle dataset downloading from Kaggle"""
    
    def __init__(self):
        """Initialize the downloader with kaggle credentials"""
        self.KAGGLE_CONFIG_DIR = Path.home() / '.kaggle'
        self.KAGGLE_JSON_FILE_PATH = self.KAGGLE_CONFIG_DIR / 'kaggle.json'
        self.DATASET_NAME = 'shaunthesheep/microsoft-catsvsdogs-dataset'
        
        # Use absolute path based on project root
        project_root = Path(__file__).parent.parent.parent
        self.DOWNLOAD_PATH = project_root / 'data' / 'raw'
        self.DATASET_EXTRACT_PATH = self.DOWNLOAD_PATH / 'PetImages'
    
    def check_kaggle_json(self):
        """Check if kaggle.json exists and has proper permissions"""
        if not self.KAGGLE_JSON_FILE_PATH.exists():
            raise cuexc(f"kaggle.json not found. Expected Location: {self.KAGGLE_JSON_FILE_PATH}", sys)
        else:
            logging.info(f"✓ File found at {self.KAGGLE_JSON_FILE_PATH}")
            try:
                self.KAGGLE_JSON_FILE_PATH.chmod(stat.S_IRUSR | stat.S_IWUSR)
                logging.info(f"✓ File permissions fixed")
            except Exception as e:
                raise cuexc(e, sys)
    
    def authenticate_kaggle(self):
        """Authenticate with Kaggle API"""
        os.environ['KAGGLE_CONFIG_DIR'] = str(self.KAGGLE_CONFIG_DIR)
        
        try:
            self.api = KaggleApi()
            self.api.authenticate()
            logging.info("✓ API successfully authenticated")
        except Exception as e:
            raise cuexc(f"Authenticate failed: {e}", sys)
    
    def is_dataset_complete(self):
        """Check if dataset is already downloaded and complete"""
        logging.info("Checking if dataset exists...")
        
        # Check if extract path exists
        logging.info(f"Checking: {self.DATASET_EXTRACT_PATH}")
        if not self.DATASET_EXTRACT_PATH.exists():
            logging.info(f"Dataset folder not found")
            return False, "Dataset folder not found"
        
        logging.info(f"Dataset folder found")
        print('Dataset Found..')
        
        # Check if Cat and Dog folders exist
        cat_folder = self.DATASET_EXTRACT_PATH / 'Cat'
        dog_folder = self.DATASET_EXTRACT_PATH / 'Dog'
        
        logging.info(f"Checking: {cat_folder}")
        logging.info(f"Checking: {dog_folder}")
        
        if not cat_folder.exists() or not dog_folder.exists():
            logging.info(f"Cat or Dog folder missing")
            return False, "Cat or Dog folder missing"
        
        logging.info(f"Both Cat and Dog folders found")
        
        # Count files in each folder (support multiple formats)
        cat_files = list(cat_folder.glob('*.*'))
        dog_files = list(dog_folder.glob('*.*'))
        
        cat_count = len([f for f in cat_files if f.suffix.lower() in ['.jpg', '.jpeg', '.png']])
        dog_count = len([f for f in dog_files if f.suffix.lower() in ['.jpg', '.jpeg', '.png']])
        
        logging.info(f"Cat images found: {cat_count}")
        logging.info(f"Dog images found: {dog_count}")
        
        if cat_count == 0 or dog_count == 0:
            logging.info(f"No images found")
            return False, "No images found in Cat or Dog folder"
        
        # If all checks pass
        total_count = cat_count + dog_count
        logging.info(f"Dataset is complete!")
        return True, f"Dataset complete - Cats: {cat_count}, Dogs: {dog_count}, Total: {total_count}"
    
    def download_dataset(self):
        """Download and extract the dataset"""
        # Check if dataset already exists and is complete
        is_complete, message = self.is_dataset_complete()
        
        if is_complete:
            logging.info(f"Dataset already downloaded!")
            logging.info(f"Location: {self.DATASET_EXTRACT_PATH.absolute()}")
            logging.info(f"{message}")
            logging.info("Download skipped - using existing dataset")
        else:
            logging.info(f"Downloading: {self.DATASET_NAME}")
            print(f"   Destination: {self.DOWNLOAD_PATH.absolute()}\n")
            
            self.DOWNLOAD_PATH.mkdir(parents=True, exist_ok=True)
            
            try:
                self.api.dataset_download_files(
                    self.DATASET_NAME,
                    path=str(self.DOWNLOAD_PATH),
                    unzip=True
                )
                logging.info("Download complete!")
                
                # Verify download
                if self.DATASET_EXTRACT_PATH.exists():
                    file_count = sum([len(files) for r, d, files in os.walk(self.DATASET_EXTRACT_PATH)])
                    logging.info(f"Dataset verified - {file_count} files found")
                else:
                    logging.warning("Dataset folder not found after extraction")
                    
            except Exception as e:
                raise cuexc(f"Error downloading: {e}", sys)
    
    def run(self):
        """Run the complete download process"""
        self.check_kaggle_json()
        self.authenticate_kaggle()
        self.download_dataset()
        return self.DATASET_EXTRACT_PATH


# if __name__ == "__main__":
#     downloader = DownloadData()
#     downloader.run()
