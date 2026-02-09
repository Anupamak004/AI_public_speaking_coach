from main import run_video_pipeline
from extract_audio_features import run_audio_pipeline
from filler_count.src.main import run_text_pipeline
import os
import numpy as np

ROOT = os.path.dirname(os.path.abspath(__file__))
VIDEO = os.path.join(ROOT, "data", "videos", "sample_video6.mp4")

# -------- VIDEO --------
video_out = run_video_pipeline(VIDEO)
video_vector = video_out["video_vector"]

# -------- AUDIO --------
audio_out = run_audio_pipeline(VIDEO)
audio_vector = audio_out["audio_vector"]

# -------- TEXT --------
text_out = run_text_pipeline(VIDEO)
text_vector = text_out["text_vector"]

# -------- FUSION --------
fusion_vector = np.concatenate([video_vector, audio_vector, text_vector])

print("VIDEO VECTOR:", video_vector)
print("AUDIO VECTOR:", audio_vector)
print("TEXT VECTOR:", text_vector)
print("FUSION VECTOR:", fusion_vector)