# 🐱 Cat vs Dog Classifier

A deep learning project that fine-tunes a pre-trained **MobileNetV2** model to classify images of cats and dogs. This project demonstrates Transfer Learning and includes a user-friendly **Streamlit** web application for real-time inference.

## ✨ Features

*   **Transfer Learning**: Utilizes MobileNetV2 (pre-trained on ImageNet) for efficient and accurate feature extraction.
*   **Fine-Tuning**: Custom top layers trained specifically for binary classification (Cat vs Dog).
*   **Web Interface**: Interactive Streamlit app for easy image uploading and prediction.
*   **Data Pipeline**: Structured data organization for training, validation, and testing.
*   **Modular Codebase**: Clean separation of concerns (Configuration, Components, Pipelines).

## 🛠️ Tech Stack

*   **Python 3.8+**
*   **TensorFlow / Keras 2.13+**
*   **Streamlit** (Web UI)
*   **NumPy & Pandas** (Data Processing)
*   **Pillow** (Image Handling)

## 📂 Project Structure

```
CNN-FineTune/
├── configs/              # Configuration files (YAML/JSON)
├── data/                 # Data directory
│   ├── raw/              # Original dataset
│   └── processed/        # Preprocessed data
├── docs/                 # Documentation
├── logs/                 # Training logs
├── models/               # Saved model checkpoints (model.h5)
├── Notebooks/            # Jupyter notebooks for experimentation
├── src/                  # Source code
│   ├── Component/        # Reusable components (Data Ingestion, Model Trainer, etc.)
│   ├── Pipeline/         # Training and inference pipelines
│   ├── logger.py         # Logging configuration
│   ├── Exception.py      # Custom exceptions
│   └── utils.py          # Utility functions
├── tests/                # Unit tests
├── app.py                # Streamlit Application Entry Point
├── requirements.txt      # Python dependencies
└── setup.py              # Package setup
```

## 🚀 Setup & Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd CNN-FineTune
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # macOS/Linux
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## 💻 Usage

### Running the Web App

To launch the Cat vs Dog Classifier interface:

```bash
streamlit run app.py
```

The app will open in your browser (usually at `http://localhost:8501`). You can upload an image (JPG, PNG) and the model will predict whether it's a Cat or a Dog along with a confidence score.

### Training the Model (Optional)

If you want to retrain the model:

1.  Ensure your data is in `data/raw/`.
2.  Run the training pipeline (example):
    ```bash
    python src/Pipeline/training_pipeline.py
    ```
    *(Note: Adjust command based on your specific pipeline file definition)*

## 📊 Model Details

*   **Base Model**: MobileNetV2 (Frozen weights)
*   **Input Shape**: (150, 150, 3)
*   **Optimization**: Adam Optimizer
*   **Loss Function**: Binary Crossentropy

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
