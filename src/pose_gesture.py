import cv2
import mediapipe as mp
import numpy as np
import os
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

class PoseGestureAnalysis:
    """
    Analyzes body pose and gestures using MediaPipe Tasks API.
    """
    def __init__(self):
        model_path = os.path.join(os.path.dirname(__file__), 'models', 'pose_landmarker_full.task')
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            num_poses=1
        )
        self.detector = vision.PoseLandmarker.create_from_options(options)

    def analyze(self, frame):
        """
        Analyze body pose.
        """
        h, w, c = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        
        detection_result = self.detector.detect(mp_image)
        
        if not detection_result.pose_landmarks:
            return {'posture_type': "Unknown", 'hands_visible': False}
            
        landmarks = detection_result.pose_landmarks[0] # List of NormalizedLandmark
        
        # Landmarks indices are same as legacy (BlazePose)
        # Left Wrist: 15, Right Wrist: 16
        left_wrist = landmarks[15]
        right_wrist = landmarks[16]
        
        hands_visible = (left_wrist.visibility > 0.5) or (right_wrist.visibility > 0.5)
        
        left_shoulder = landmarks[11]
        right_shoulder = landmarks[12]
        
        is_crossed = False
        if left_wrist.visibility > 0.5 and right_wrist.visibility > 0.5:
            wrist_dist = abs(left_wrist.x - right_wrist.x)
            if wrist_dist < 0.1:
                is_crossed = True
                
        posture_type = "Closed" if is_crossed else "Open"
        
        return {
            'posture_type': posture_type,
            'hands_visible': hands_visible,
            'landmarks': landmarks 
        }
