import numpy as np

from main import run_video_pipeline
from extract_audio_features import run_audio_pipeline
from filler_count.src.main import run_text_pipeline
from fusion.multimodal_fusion import MultimodalFusionEngine


def main():
    video_path = "data/videos/sample_video.mp4"

    print("\n--- Running Pipelines ---")
    video_res = run_video_pipeline(video_path)
    audio_res = run_audio_pipeline(video_path)
    text_res  = run_text_pipeline(video_path)

    # -------- FORCE CONSISTENT TYPES --------
    audio_vec = np.asarray(audio_res["audio_vector"], dtype=np.float32)
    video_vec = np.asarray(video_res["video_vector"], dtype=np.float32)
    text_vec  = np.asarray(text_res["text_vector"], dtype=np.float32)

    # -------- Shape checks --------
    print("\n--- Feature Shapes ---")
    print("Audio:", audio_vec.shape)
    print("Video:", video_vec.shape)
    print("Text :", text_vec.shape)

    assert audio_vec.ndim == 1
    assert video_vec.ndim == 1
    assert text_vec.ndim == 1

    assert not np.isnan(audio_vec).any()
    assert not np.isnan(video_vec).any()
    assert not np.isnan(text_vec).any()

    # -------- Fusion --------
    fusion_engine = MultimodalFusionEngine(
        audio_dim=len(audio_vec),
        video_dim=len(video_vec),
        text_dim=len(text_vec)
    )

    fusion_vec = fusion_engine.fuse(
        audio_vec,
        video_vec,
        text_vec
    )

    print("\n--- Fusion Output ---")
    print("Fusion vector shape:", fusion_vec.shape)
    print("Fusion vector (first 10 values):", fusion_vec[:10])

    assert fusion_vec.shape == (128,)
    assert not np.isnan(fusion_vec).any()

    print("\n✅ Integration successful! Everything is correct.")


if __name__ == "__main__":
    main()
