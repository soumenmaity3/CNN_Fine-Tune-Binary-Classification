import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { FiUploadCloud, FiCheckCircle, FiAlertCircle } from 'react-icons/fi';

const API_URL = 'http://localhost:5000/predict';

function App() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const onDrop = (acceptedFiles) => {
    const selectedFile = acceptedFiles[0];
    setFile(selectedFile);
    setPreview(URL.createObjectURL(selectedFile));
    setPrediction(null);
    setError(null);
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.webp']
    },
    multiple: false
  });

  const handlePredict = async () => {
    if (!file) return;

    setLoading(true);
    setError(null);

    const checkBackend = async () => {
      try {
        // A simple health check or just proceeding
      } catch (err) {
        console.error(err);
      }
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(API_URL, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setPrediction(response.data);
    } catch (err) {
      console.error(err);
      setError('Failed to get prediction. Ensure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-950 text-white flex flex-col items-center justify-center p-4">
      <motion.h1
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-4xl md:text-5xl font-extrabold mb-8 text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-600"
      >
        Cat vs Dog Classifier
      </motion.h1>

      <div className="w-full max-w-md bg-gray-900 rounded-2xl shadow-xl overflow-hidden border border-gray-800">
        <div className="p-8">

          {/* Dropzone */}
          <div
            {...getRootProps()}
            className={`flex flex-col items-center justify-center w-full h-48 border-2 border-dashed rounded-xl cursor-pointer transition-colors duration-200 
              ${isDragActive ? 'border-blue-500 bg-gray-800' : 'border-gray-700 hover:border-blue-400 hover:bg-gray-800'}`}
          >
            <input {...getInputProps()} />
            {preview ? (
              <img
                src={preview}
                alt="Preview"
                className="h-full w-full object-cover rounded-xl opacity-80"
              />
            ) : (
              <div className="text-center text-gray-400">
                <FiUploadCloud className="w-10 h-10 mx-auto mb-2 text-gray-500" />
                <p className="text-sm">Drag & drop or click to select</p>
                <p className="text-xs text-gray-600 mt-1">JPEG, PNG, WEBP</p>
              </div>
            )}
          </div>

          {/* Action Button */}
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={handlePredict}
            disabled={!file || loading}
            className={`w-full mt-6 py-3 rounded-xl font-bold text-lg shadow-lg transition-all
              ${!file
                ? 'bg-gray-800 text-gray-600 cursor-not-allowed'
                : 'bg-gradient-to-r from-blue-500 to-purple-600 text-white hover:shadow-blue-500/25'
              }
              ${loading ? 'opacity-70 cursor-wait' : ''}
            `}
          >
            {loading ? 'Analyzing...' : 'Predict'}
          </motion.button>

          {/* Error Message */}
          {error && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="mt-4 p-3 bg-red-900/50 border border-red-700/50 rounded-lg flex items-center gap-2 text-red-200 text-sm"
            >
              <FiAlertCircle />
              {error}
            </motion.div>
          )}

          {/* Results */}
          <AnimatePresence>
            {prediction && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                className="mt-6 pt-6 border-t border-gray-800"
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="text-gray-400 text-sm">Verdict</span>
                  <span className="text-gray-400 text-sm">Confidence</span>
                </div>

                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <span className="text-3xl">
                      {prediction.class === 'Cat' ? '🐱' : '🐶'}
                    </span>
                    <span className={`text-2xl font-bold ${prediction.class === 'Cat' ? 'text-blue-400' : 'text-purple-400'}`}>
                      {prediction.class}
                    </span>
                  </div>
                  <div className="text-2xl font-bold">
                    {(prediction.confidence).toLocaleString(undefined, { style: 'percent', minimumFractionDigits: 1 })}
                  </div>
                </div>

                {/* Progress Bar */}
                <div className="w-full bg-gray-800 h-2 rounded-full mt-4 overflow-hidden">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${prediction.confidence * 100}%` }}
                    transition={{ duration: 0.8, ease: "easeOut" }}
                    className={`h-full ${prediction.class === 'Cat' ? 'bg-blue-500' : 'bg-purple-500'}`}
                  />
                </div>
              </motion.div>
            )}
          </AnimatePresence>

        </div>
      </div>

      <div className="mt-8 text-gray-600 text-xs">
        Powered by Tensorflow & React
      </div>
    </div>
  );
}

export default App;
