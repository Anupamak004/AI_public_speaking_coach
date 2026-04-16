import cv2
import mediapipe as mp
import numpy as np
import os
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

class FaceAnalysis:
    """
    Handles Face Detection, Landmark Extraction, and Head Pose Estimation using MediaPipe Tasks API.
    """
    def __init__(self):
        """Initialize MediaPipe Face Landmarker."""
        # Use absolute path to model file
        model_path = os.path.join(os.path.dirname(__file__), 'models', 'face_landmarker.task')
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.FaceLandmarkerOptions(
            base_options=base_options,
            output_face_blendshapes=True,
            output_facial_transformation_matrixes=True,
            num_faces=1
        )
        self.detector = vision.FaceLandmarker.create_from_options(options)

    def analyze(self, frame):
        """
        Process a frame to detect face and head pose.
        
        Args:
            frame: BGR image from OpenCV.
            
        Returns:
            dict: {
                'landmarks': list of (x, y, z),
                'head_pose': {'yaw': float, 'pitch': float, 'roll': float},
                'face_detected': bool
            }
        """
        h, w, c = frame.shape
        # Tasks API expects MP Image
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        
        detection_result = self.detector.detect(mp_image)
        
        if not detection_result.face_landmarks:
            return {'face_detected': False}
            
        # Get first face
        landmarks = detection_result.face_landmarks[0] # List of NormalizedLandmark
        
        # Convert to list tuples for consumption
        landmark_points = []
        for lm in landmarks:
            landmark_points.append((lm.x, lm.y, lm.z))
            
        # Head Pose Estimation via Transformation Matrix
        # The new API provides facial_transformation_matrixes if enabled!
        # Matrix is 4x4.
        head_pose = None
        if detection_result.facial_transformation_matrixes:
            matrix = detection_result.facial_transformation_matrixes[0] # numpy 4x4
            
            # Extract Euler Angles from Rotation Matrix
            # Matrix is [R | T]
            #           [0 | 1]
            # We care about R (top-left 3x3)
            rmat = matrix[:3, :3]
            
            # Decompose rotation matrix to Euler angles
            # Similar to CV2 RQDecomp3x3 or manual calculation
            # Note: MediaPipe matrix might be in a specific convention (OpenGL?)
            
            # Let's use cv2.RQDecomp3x3
            angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)
            
            # angles are in degrees? usually.
            x = angles[0] # Pitch
            y = angles[1] # Yaw
            z = angles[2] # Roll
            
            # Depending on convention, needed to scale / offset?
            # Usually direct RQDecomp of the proper R matrix gives degrees.
            
            head_pose = {'pitch': x * 1.0, 'yaw': y * 1.0, 'roll': z * 1.0}
        
        if head_pose is None:
             # Fallback to PnP if matrix not available (but it should be)
             # Reuse old PnP logic? The landmarks are available.
             pass

        return {
            'face_detected': True,
            'landmarks': landmark_points,
            'head_pose': head_pose
        }
