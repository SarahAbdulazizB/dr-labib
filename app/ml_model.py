# app/ml_model.py
"""
Machine Learning Model for Sign Language Translation
Uses pre-loaded LSTM model and label encoder
"""
import numpy as np
from flask import current_app

class SignLanguageModel:
    def __init__(self):
        """Initialize model (actual models loaded in app/__init__.py)"""
        self.model = None
        self.label_encoder = None
    
    def translate_video(self, npy_file_path):
        """
        Translates sign language keypoints to text
        
        Args:
            npy_file_path (str): Path to .npy keypoint file
            
        Returns:
            tuple: (success: bool, prediction: str or error_message: str)
            
        Raises:
            Exception: If model not loaded or prediction fails
        """
        try:
            # Get pre-loaded model and encoder from app config
            lstm_model = current_app.config.get('LSTM_MODEL')
            label_encoder = current_app.config.get('LABEL_ENCODER')
            
            # Validate models are loaded
            if lstm_model is None:
                return False, "Model not loaded. Please contact administrator."
            
            if label_encoder is None:
                return False, "Label encoder not loaded. Please contact administrator."
            
            # Load keypoint data from .npy file
            try:
                keypoints = np.load(npy_file_path)
            except FileNotFoundError:
                return False, "Keypoint file not found."
            except Exception as e:
                return False, f"Failed to load keypoint file: {str(e)}"
            
            # Validate keypoint shape (should be 80, 258)
            if keypoints.ndim != 2:
                return False, f"Invalid keypoint dimensions. Expected 2D array, got {keypoints.ndim}D."
            
            if keypoints.shape[0] != 80:
                return False, f"Invalid frame count. Expected 80 frames, got {keypoints.shape[0]}."
            
            if keypoints.shape[1] != 258:
                return False, f"Invalid keypoint features. Expected 258, got {keypoints.shape[1]}."
            
            # Add batch dimension: (80, 258) → (1, 80, 258)
            keypoints_batch = np.expand_dims(keypoints, axis=0)
            
            # Run inference
            try:
                predictions = lstm_model.predict(keypoints_batch, verbose=0)
            except Exception as e:
                return False, f"Model inference failed: {str(e)}"
            
            # Get predicted class (argmax)
            pred_class = np.argmax(predictions, axis=1)[0]
            
            # Convert class index to sentence using label encoder
            try:
                predicted_sentence = label_encoder.inverse_transform([pred_class])[0]
            except Exception as e:
                return False, f"Failed to decode prediction: {str(e)}"
            
            return True, predicted_sentence
        
        except Exception as e:
            return False, f"Translation error: {str(e)}"
    
    def is_model_ready(self):
        """Check if models are loaded and ready"""
        lstm_model = current_app.config.get('LSTM_MODEL')
        label_encoder = current_app.config.get('LABEL_ENCODER')
        return lstm_model is not None and label_encoder is not None

# Create singleton instance
model = SignLanguageModel()