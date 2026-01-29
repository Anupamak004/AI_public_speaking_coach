import os
import numpy as np
import librosa
from moviepy.editor import VideoFileClip

# -----------------------------
# Paths
# -----------------------------
VIDEO_PATH = "data/videos/sample.mp4"
AUDIO_PATH = "data/audio/sample.wav"

# -----------------------------
# Extract Audio from Video
# -----------------------------
def extract_audio(video_path, audio_path):
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path, verbose=False, logger=None)
    video.close()
    print(f"Audio saved to {audio_path}")

# -----------------------------
# Audio Feature Extraction
# -----------------------------
def extract_audio_features(audio_path):
    y, sr = librosa.load(audio_path, sr=None)

    # Duration
    duration = librosa.get_duration(y=y, sr=sr)

    # Silence / Pause Ratio
    intervals = librosa.effects.split(y, top_db=25)
    voiced_duration = sum((end - start) for start, end in intervals) / sr
    pause_ratio = 1 - (voiced_duration / duration)

    # Energy
    energy = np.square(y)
    energy_mean = np.mean(energy)
    energy_variance = np.var(energy)

    # Pitch (Fundamental Frequency)
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    pitch_values = pitches[magnitudes > np.max(magnitudes) * 0.1]
    pitch_mean = np.mean(pitch_values) if len(pitch_values) > 0 else 0

    # Speech Rate (words per minute – estimated)
    syllable_peaks = librosa.onset.onset_detect(y=y, sr=sr)
    speech_rate = (len(syllable_peaks) / duration) * 60

    # -----------------------------
    # MFCC (ADDED ONLY)
    # -----------------------------
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc_mean = np.mean(mfcc, axis=1)
    mfcc_variance = np.var(mfcc, axis=1)

    # Simple Emotion Inference (UNCHANGED)
    if energy_mean < 0.0003 and pause_ratio > 0.25:
        emotion = "Nervous / Low Confidence"
    elif energy_mean > 0.001 and speech_rate > 150:
        emotion = "High Arousal (Angry / Excited)"
    else:
        emotion = "Neutral / Confident"

    # -----------------------------
    # Print Results
    # -----------------------------
    print(f"\nAudio Duration        : {duration:.2f} seconds")
    print(f"Pause Ratio           : {pause_ratio:.2f}")
    print(f"Energy Mean           : {energy_mean:.6f}")
    print(f"Energy Variance       : {energy_variance:.6f}")
    print(f"Pitch Mean            : {pitch_mean:.2f} Hz")
    print(f"Speech Rate           : {speech_rate:.2f} WPM")
    print(f"Detected Emotion      : {emotion}")
    print(f"MFCC Means            : {mfcc_mean}")
    print(f"MFCC Variances        : {mfcc_variance}")

# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    extract_audio(VIDEO_PATH, AUDIO_PATH)
    extract_audio_features(AUDIO_PATH)
