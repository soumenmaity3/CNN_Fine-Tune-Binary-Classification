import sys
from pathlib import Path
import logging

# Add project root to path so imports work correctly
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.Exception import CustomException as cuexc
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

class ShowSamples:
    def __init__(self):
        # Use pathlib for path handling
        self.project_root = Path(__file__).parent.parent.parent
        self.train_dir = self.project_root / 'data' / 'processed' / 'cat-dog-split' / 'train'
        
        try:
            self.show_image(train_dir=self.train_dir)
        except Exception as e:
            logging.error(f"Error in ShowSamples: {e}")
            raise cuexc(e, sys)

    def show_image(self, train_dir):
        logging.info(f"Showing sample images from {train_dir}")
        
        train_cat_dir = train_dir / 'Cat'
        train_dog_dir = train_dir / 'Dog'

        # Check if directories exist
        if not train_cat_dir.exists() or not train_dog_dir.exists():
            error_msg = f"Train directories not found at {train_cat_dir} or {train_dog_dir}"
            logging.error(error_msg)
            print(error_msg)
            return

        # Get list of jpg files
        train_cat_fname = [f for f in train_cat_dir.glob('*.jpg')]
        train_dog_fname = [f for f in train_dog_dir.glob('*.jpg')]

        sample_dog = train_dog_fname[:5]
        sample_cat = train_cat_fname[:5]
        
        if not sample_cat or not sample_dog:
            logging.warning("Not enough images found to plot.")
            return

        plt.figure(figsize=(12, 6))

        # Plot Cats
        for i, img_path in enumerate(sample_cat):
            try:
                img = mpimg.imread(str(img_path))
                plt.subplot(2, 5, i + 1) # 2 rows, 5 columns, index 1-5
                plt.imshow(img)
                plt.title('Cat')
                plt.axis('off')
            except Exception as e:
                logging.warning(f"Could not load image {img_path}: {e}")

        # Plot Dogs
        for i, img_path in enumerate(sample_dog):
            try:
                img = mpimg.imread(str(img_path))
                plt.subplot(2, 5, i + 6) # 2 rows, 5 columns, index 6-10
                plt.imshow(img)
                plt.title('Dog')
                plt.axis('off')
            except Exception as e:
                logging.warning(f"Could not load image {img_path}: {e}")

        output_file = 'sample_images.png'
        # Save to the current working directory or a specific artifact folder
        # If user wanted to make a directory:
        # (Path.cwd() / 'data' / 'sample').mkdir(parents=True, exist_ok=True)
        # but sticking to simple save for now as per previous working intent
        
        plt.savefig(output_file)
        logging.info(f"Sample images saved to {output_file}")
        print(f"Sample images saved to {output_file}")

if __name__ == "__main__":
    try:
        ShowSamples()
    except Exception as e:
        print(f"Execution failed: {e}")