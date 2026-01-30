import cv2
import numpy as np
import os

def create_dummy_video(filename="input_videos/dummy.mp4", duration=5, fps=30):
    output_dir = os.path.dirname(filename)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    height, width = 720, 1280
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(filename, fourcc, fps, (width, height))
    
    frames = duration * fps
    
    print(f"Generating {filename} ({duration}s, {fps}fps)...")
    
    for i in range(frames):
        # Create a black image
        img = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Draw a moving circle (simulating movement)
        x = int((i / frames) * width)
        y = height // 2
        cv2.circle(img, (x, y), 50, (0, 255, 0), -1)
        
        # Draw something that looks vaguely like a face? (Circle + eyes)
        # Center face
        cx, cy = width // 2, height // 2
        cv2.circle(img, (cx, cy), 150, (200, 200, 200), -1) # Face
        cv2.circle(img, (cx - 50, cy - 30), 20, (0, 0, 0), -1) # Left Eye
        cv2.circle(img, (cx + 50, cy - 30), 20, (0, 0, 0), -1) # Right Eye
        cv2.ellipse(img, (cx, cy + 50), (60, 20), 0, 0, 180, (0, 0, 0), 5) # Mouth
        
        out.write(img)
        
    out.release()
    print("Video generation complete.")

if __name__ == "__main__":
    create_dummy_video()
