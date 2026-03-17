# run_inference.py
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
from feedback.feedback_engine import generate_feedback

DEVICE = "cpu"

# -------- Global cached models --------
amfn = None
temporal = None


# -------- Load models ONCE --------
def load_models(audio_dim, video_dim, text_dim):
    global amfn, temporal

    if amfn is not None and temporal is not None:
        return

    amfn = AMFN(audio_dim, video_dim, text_dim).to(DEVICE)
    temporal = TemporalBiLSTM(input_dim=128).to(DEVICE)

    amfn.load_state_dict(torch.load("amfn_trained.pth", map_location=DEVICE))
    temporal.load_state_dict(torch.load("temporal_trained.pth", map_location=DEVICE))

    amfn.eval()
    temporal.eval()


# -------- Main inference --------
def run_inference(video_path: str):

    # -------- Run pipelines ONCE --------
    video_res = run_video_pipeline(video_path)
    audio_res = run_audio_pipeline(video_path)
    text_res  = run_text_pipeline(video_path)

    audio_vec = np.asarray(audio_res["audio_vector"], dtype=np.float32)
    video_vec = np.asarray(video_res["video_vector"], dtype=np.float32)
    text_vec  = np.asarray(text_res["text_vector"], dtype=np.float32)

    # -------- Load models using extracted dimensions --------
    load_models(
        audio_dim=len(audio_vec),
        video_dim=len(video_vec),
        text_dim=len(text_vec)
    )

    # -------- Temporal segmentation (kept for same behavior) --------
    segments = segment_video(video_path, window_size=5)
    seq_len = len(segments)

    with torch.no_grad():
        a = torch.tensor(audio_vec).unsqueeze(0)
        v = torch.tensor(video_vec).unsqueeze(0)
        t = torch.tensor(text_vec).unsqueeze(0)

        # -------- Fusion ONCE --------
        fusion = amfn(a, v, t)  # (1, 128)

        # -------- Repeat only for temporal input shape --------
        fusion_seq = fusion.unsqueeze(1).repeat(1, seq_len, 1)

        _, preds = temporal(fusion_seq)
        preds = torch.sigmoid(preds) * 10.0

    # -------- Post-processing (unchanged) --------
    scores = np.rint(preds.squeeze().cpu().numpy()).astype(int)
    scores = np.clip(scores, 0, 10)

    labels = ["Confidence", "Clarity", "Fluency", "Engagement", "Nervousness"]
    results = dict(zip(labels, scores.tolist()))

    feature_context = {
        "audio": audio_res,
        "video": video_res,
        "text": text_res
    }

    feedback_data = generate_feedback(results)
    return {
        "scores": results,
        **feedback_data
    }