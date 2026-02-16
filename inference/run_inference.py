import numpy as np
import torch
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT)

from models.amfn import AMFN
from temporal.temporal_model import TemporalBiLSTM
from sequence.segmenter import segment_video
from main import run_video_pipeline
from extract_audio_features import run_audio_pipeline
from filler_count.src.main import run_text_pipeline


DEVICE = "cpu"
VIDEO_PATH = "data/videos/v18.mp4"

# -------- Load models --------
audio_dim =  len(run_audio_pipeline(VIDEO_PATH)["audio_vector"])
video_dim =  len(run_video_pipeline(VIDEO_PATH)["video_vector"])
text_dim  =  len(run_text_pipeline(VIDEO_PATH)["text_vector"])

amfn = AMFN(audio_dim, video_dim, text_dim).to(DEVICE)
temporal = TemporalBiLSTM(input_dim=128).to(DEVICE)

amfn.load_state_dict(torch.load("amfn_trained.pth", map_location=DEVICE))
temporal.load_state_dict(torch.load("temporal_trained.pth", map_location=DEVICE))

amfn.eval()
temporal.eval()

# -------- Segment video --------
segments = segment_video(VIDEO_PATH, window_size=5)

# -------- Extract features once --------
video_res = run_video_pipeline(VIDEO_PATH)
audio_res = run_audio_pipeline(VIDEO_PATH)
text_res  = run_text_pipeline(VIDEO_PATH)

audio_vec = np.asarray(audio_res["audio_vector"], dtype=np.float32)
video_vec = np.asarray(video_res["video_vector"], dtype=np.float32)
text_vec  = np.asarray(text_res["text_vector"], dtype=np.float32)

# -------- Build fusion sequence --------
fusion_seq = []

with torch.no_grad():
    for _ in segments:
        a = torch.tensor(audio_vec).unsqueeze(0)
        v = torch.tensor(video_vec).unsqueeze(0)
        t = torch.tensor(text_vec).unsqueeze(0)

        fusion = amfn(a, v, t)
        fusion_seq.append(fusion)

    fusion_seq = torch.stack(fusion_seq, dim=1)  # (1, T, 128)
    _, preds = temporal(fusion_seq)
    preds = torch.sigmoid(preds) * 10.0

scores = np.rint(preds.squeeze().numpy()).astype(int)
scores = np.clip(scores, 0, 10)

print("\n--- Predicted Public Speaking Scores ---")
labels = ["Confidence", "Clarity", "Fluency", "Engagement", "Nervousness"]
for l, s in zip(labels, scores):
    print(f"{l}: {s}/10")

