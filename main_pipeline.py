import numpy as np
import torch

from fusion.multimodal_fusion import MultimodalFusionEngine
from extract_audio_features import run_audio_pipeline
from main import run_video_pipeline
from filler_count.src.main import run_text_pipeline
from temporal.temporal_model import TemporalBiLSTM
from prediction.predictor import PerformancePredictor
from prediction.feedback_generator import FeedbackGenerator

# ------------------- Pipeline -------------------
video_path = "data/videos/sample_video.mp4"

# Step 1: Feature extraction
video_res = run_video_pipeline(video_path)
audio_res = run_audio_pipeline(video_path)
text_res  = run_text_pipeline(video_path)

audio_vec = np.asarray(audio_res["audio_vector"], dtype=np.float32)
video_vec = np.asarray(video_res["video_vector"], dtype=np.float32)
text_vec  = np.asarray(text_res["text_vector"], dtype=np.float32)

# Step 2: Multimodal fusion
fusion_engine = MultimodalFusionEngine(
    audio_dim=len(audio_vec),
    video_dim=len(video_vec),
    text_dim=len(text_vec)
)

fusion_vec = fusion_engine.fuse(audio_vec, video_vec, text_vec)
fusion_vec = torch.tensor(fusion_vec).unsqueeze(0).unsqueeze(0)  # (1, 1, 128)

# Step 3: Temporal modeling (simulate 10 segments)
B, T, D = 1, 10, 128
fusion_sequence = fusion_vec.repeat(1, T, 1)  # replicate vector for segments
temporal_model = TemporalBiLSTM(input_dim=D)
temporal_out = temporal_model(fusion_sequence)

# Step 4: Predict performance scores
predictor = PerformancePredictor(input_dim=D)
predictor.eval()
with torch.no_grad():
    scores = predictor(temporal_out).numpy().squeeze()  # shape (5,)

# Step 5: Generate feedback
feedback_gen = FeedbackGenerator()
result = feedback_gen.generate_feedback(scores)

print("\n--- Predicted Scores ---")
for k, v in result["scores"].items():
    print(f"{k}: {v}")

print("\n--- Feedback ---")
for fb in result["feedback"]:
    print("-", fb)
