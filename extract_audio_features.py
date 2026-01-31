import numpy as np
import librosa
from moviepy import VideoFileClip
from pathlib import Path

import parselmouth
import parselmouth.praat as praat

# -----------------------------
# Paths
# -----------------------------
VIDEO_PATH = "data/videos/sample_video6.mp4"
AUDIO_PATH = "data/audio/sample.wav"

# -----------------------------
# Extract Audio from Video
# -----------------------------
def extract_audio(video_path, audio_path):
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path, logger=None)
    video.close()
    print(f"Audio saved to {audio_path}")

# -----------------------------
# PRAAT FEATURES (GROUND TRUTH)
# -----------------------------
def extract_praat_features(audio_path):
    sound = parselmouth.Sound(audio_path)

    # Pitch
    pitch = sound.to_pitch(pitch_floor=75, pitch_ceiling=300)
    mean_pitch = praat.call(pitch, "Get mean", 0, 0, "Hertz")
    pitch_std = praat.call(pitch, "Get standard deviation", 0, 0, "Hertz")

    # Intensity
    intensity = sound.to_intensity()
    mean_energy = praat.call(intensity, "Get mean", 0, 0)
    energy_std = praat.call(intensity, "Get standard deviation", 0, 0)

    # PointProcess for voice quality
    point_process = praat.call(
        sound,
        "To PointProcess (periodic, cc)",
        75,
        300
    )

    jitter = praat.call(
        point_process,
        "Get jitter (local)",
        0, 0,
        0.0001,
        0.02,
        1.3
    )

    shimmer = praat.call(
        [sound, point_process],
        "Get shimmer (local)",
        0, 0,
        0.0001,
        0.02,
        1.3,
        1.6
    )

    return {
        "praat_mean_pitch": mean_pitch,
        "praat_pitch_std": pitch_std,
        "praat_mean_energy": mean_energy,
        "praat_energy_std": energy_std,
        "jitter": jitter,
        "shimmer": shimmer
    }


# -----------------------------
# LIBROSA FEATURES (ML-FRIENDLY)
# -----------------------------
def extract_librosa_features(audio_path):
    y, sr = librosa.load(audio_path, sr=None)
    duration = librosa.get_duration(y=y, sr=sr)

    # Silence / Pause Ratio
    intervals = librosa.effects.split(y, top_db=25)
    voiced_duration = sum((end - start) for start, end in intervals) / sr
    pause_ratio = 1 - (voiced_duration / duration) if duration > 0 else 0

    # Energy (RMS → dB)
    rms = librosa.feature.rms(y=y)[0]
    rms_db = librosa.amplitude_to_db(rms, ref=np.max)

    energy_mean = np.mean(rms_db)
    energy_std = np.std(rms_db)

    # Pitch (YIN – speech range)
    f0 = librosa.yin(
        y,
        fmin=75,
        fmax=300,
        sr=sr,
        frame_length=2048,
        hop_length=512
    )

    f0 = f0[~np.isnan(f0)]
    pitch_mean = np.mean(f0)
    pitch_std = np.std(f0)


    # Speech Rate (approx.)
    syllable_count = len(intervals)
    word_count = syllable_count / 1.5 if syllable_count > 0 else 0
    speech_rate = (word_count / duration) * 60 if duration > 0 else 0

    # MFCCs
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc_mean = np.mean(mfcc, axis=1)
    mfcc_var = np.var(mfcc, axis=1)

    return {
        "duration": duration,
        "pause_ratio": pause_ratio,
        "librosa_mean_pitch": pitch_mean,
        "librosa_pitch_std": pitch_std,
        "librosa_mean_energy": energy_mean,
        "librosa_energy_std": energy_std,
        "speech_rate": speech_rate,
        "mfcc_mean": mfcc_mean,
        "mfcc_var": mfcc_var
    }

# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    extract_audio(VIDEO_PATH, AUDIO_PATH)

    praat_features = extract_praat_features(AUDIO_PATH)
    librosa_features = extract_librosa_features(AUDIO_PATH)

    print("\n--- PRAAT FEATURES (Ground Truth) ---")
    for k, v in praat_features.items():
        print(f"{k}: {v}")

    print("\n--- LIBROSA FEATURES (Praat-like) ---")
    for k, v in librosa_features.items():
        print(f"{k}: {v}")
