import cv2
import os

class VideoReader:
    """
    Handles video file reading and frame sampling.
    """
    def __init__(self, video_path: str, target_fps: int = 5):
        """
        Initialize the VideoReader.

        Args:
            video_path (str): Path to the input video file.
            target_fps (int): Desired frames per second for sampling.
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        self.video_path = video_path
        self.target_fps = target_fps
        self.cap = cv2.VideoCapture(video_path)
        
        if not self.cap.isOpened():
            raise IOError(f"Could not open video file: {video_path}")
            
        self.original_fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.duration_sec = self.total_frames / self.original_fps if self.original_fps > 0 else 0
        
        # Calculate frame skip interval
        if self.original_fps > 0:
            self.skip_frames = int(self.original_fps / self.target_fps)
        else:
            self.skip_frames = 1  # Fallback
            
        # Ensure we don't skip to 0
        self.skip_frames = max(1, self.skip_frames)

    def get_frames(self):
        """
        Generator that yields sampled frames.
        
        Yields:
            frame_count (int): The current frame number (original).
            frame (numpy.ndarray): The sampled frame image.
        """
        frame_idx = 0
        sampled_count = 0
        
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break
            
            # Simple sampling: keep frame if current index is a multiple of skip_frames
            # Or better: keep if (frame_idx % skip_frames) == 0
            # To be more precise with float FPS, we could track timestamps, but integer skip is usually sufficient.
            
            if frame_idx % self.skip_frames == 0:
                yield frame_idx, frame
                sampled_count += 1
                
            frame_idx += 1
            
        self.cap.release()

    def get_info(self):
        """Returns video metadata."""
        return {
            "video_path": self.video_path,
            "original_fps": self.original_fps,
            "total_frames": self.total_frames,
            "duration_sec": self.duration_sec,
            "target_fps": self.target_fps,
            "skip_frames": self.skip_frames
        }
