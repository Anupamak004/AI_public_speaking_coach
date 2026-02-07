from deepface import DeepFace
import cv2
import logging

# Configure logging to suppress DeepFace typical verbosity if possible
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

class EmotionAnalysis:
    """
    Handles Facial Emotion Detection using DeepFace.
    """
    def __init__(self):
        # Load model once if possible or just use analyze directly.
        # DeepFace loads lazily usually.
        # We can run a dummy inference to warm up.
        pass

    def analyze(self, frame):
        """
        Analyze emotion in the frame.
        
        Args:
            frame: BGR image.
        
        Returns:
            dict: {'dominant_emotion': str, 'confidence': float, 'distribution': dict} or None
        """
        try:
            # Enforce detection = False to speed up if we already know face exists?
            # But DeepFace needs to crop the face. 
            # If we pass the full frame, it runs face detection (mtcnn, ssd, opencv etc).
            # To be fast on CPU, use backend='opencv' or 'ssd'.
            
            objs = DeepFace.analyze(
                img_path=frame, 
                actions=['emotion'], 
                enforce_detection=False, # We might handle detection failure gracefully
                detector_backend='opencv', # Lightweight backend
                silent=True
            )
            
            if not objs:
                return None
                
            # DeepFace returns a list of result dicts
            result = objs[0]
            
            return {
                'dominant_emotion': result['dominant_emotion'],
                'confidence': result.get('face_confidence', 0), # Note: face_confidence depends on backend
                'distribution': result['emotion']
            }
        except Exception as e:
            # logging.error(f"Emotion analysis error: {e}")
            return None
