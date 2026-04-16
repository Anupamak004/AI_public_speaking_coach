import os
import json
import librosa
import numpy as np
from moviepy import VideoFileClip

try:
    import webrtcvad
except ImportError:
    webrtcvad = None

import whisper_timestamped as whisper


def run_filler_pipeline(video_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    audio_path = os.path.join(output_dir, "audio.wav")
    transcript_json = os.path.join(output_dir, "transcript.json")
    filler_json = os.path.join(output_dir, "filler_report.json")

    # ==================================================
    # 1. AUDIO EXTRACTION
    # ==================================================
    print("🔊 Extracting audio...")
    VideoFileClip(video_path).audio.write_audiofile(
        audio_path, fps=16000, logger=None
    )

    # ==================================================
    # 2. LOAD AUDIO
    # ==================================================
    y, sr = librosa.load(audio_path, sr=16000)
    audio_duration_sec = librosa.get_duration(y=y, sr=sr)

    # ==================================================
    # 3. TRANSCRIPTION (TEXT ONLY)
    # ==================================================
    print("📝 Transcribing (text only)...")
    model = whisper.load_model("tiny", device="cpu")

    result = whisper.transcribe(
        model,
        audio_path,
        language="en"
    )

    full_text = " ".join(seg["text"] for seg in result["segments"])

    with open(transcript_json, "w", encoding="utf-8") as f:
        json.dump({
            "full_text": full_text,
            "segments": result["segments"]
        }, f, indent=4)

    # ==================================================
    # 4. AUDIO-BASED FILLER DETECTION (ACTUAL WORKING PART)
    # ==================================================
    print("🎧 Detecting fillers from audio...")

    frame_ms = 30
    frame_len = int(sr * frame_ms / 1000)

    if webrtcvad is not None:
        vad = webrtcvad.Vad(2)

        def is_voiced(frame):
            pcm = (frame * 32767).astype(np.int16).tobytes()
            return vad.is_speech(pcm, sr)
    else:
        print("⚠️ webrtcvad not installed; using RMS fallback for voice detection")

        def is_voiced(frame):
            rms = np.sqrt(np.mean(frame ** 2))
            return rms > 0.003

    filler_segments = []
    t = 0

    while t + frame_len < len(y):
        frame = y[t:t + frame_len]
        start = t / sr
        end = (t + frame_len) / sr

        if is_voiced(frame):
            rms = np.sqrt(np.mean(frame ** 2))
            zcr = librosa.feature.zero_crossing_rate(frame)[0][0]

            # filler-like acoustic profile
            if rms < 0.035 and zcr < 0.09:
                filler_segments.append((start, end))

        t += frame_len

    # ==================================================
    # 5. MERGE CONTIGUOUS SEGMENTS
    # ==================================================
    merged = []
    for seg in filler_segments:
        if not merged or seg[0] - merged[-1][1] > 0.25:
            merged.append(list(seg))
        else:
            merged[-1][1] = seg[1]

    # ==================================================
    # 6. FILTER BY DURATION
    # ==================================================
    fillers = []
    for s, e in merged:
        dur = e - s
        if 0.2 <= dur <= 1.2:
            fillers.append({
                "start": round(s, 2),
                "end": round(e, 2),
                "duration": round(dur, 2)
            })

    # ==================================================
    # 7. SAVE FILLER REPORT
    # ==================================================
    with open(filler_json, "w", encoding="utf-8") as f:
        json.dump({
            "total_fillers": len(fillers),
            "fillers": fillers
        }, f, indent=4)

    print("✅ Pipeline complete")
    print(f"📊 Detected fillers: {len(fillers)}")

    # ==================================================
    # 8. RETURN (COMPATIBLE WITH YOUR EXISTING PIPELINE)
    # ==================================================
    return transcript_json, audio_duration_sec, filler_json
