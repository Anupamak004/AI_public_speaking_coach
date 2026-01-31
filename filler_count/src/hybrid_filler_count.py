import os
import json
import librosa
import numpy as np
from moviepy import VideoFileClip
import whisper_timestamped as whisper
import webrtcvad

def run_filler_pipeline(video_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    audio_path = os.path.join(output_dir, "audio.wav")
    transcript_json = os.path.join(output_dir, "transcript.json")
    filler_json = os.path.join(output_dir, "filler_report.json")

    # -------- AUDIO EXTRACTION --------
    print("🔊 Extracting audio...")
    VideoFileClip(video_path).audio.write_audiofile(audio_path, logger=None)

    # -------- LOAD AUDIO --------
    y, sr = librosa.load(audio_path, sr=16000)
    audio_duration_sec = librosa.get_duration(y=y, sr=sr)


    # -------- TRANSCRIBE --------
    print("📝 Transcribing...")
    model = whisper.load_model("tiny", device="cpu")
    result = whisper.transcribe(
        model,
        y,
        language="en",
        detect_disfluencies=True
    )

    # -------- SAVE TRANSCRIPT --------
    full_text = " ".join(seg["text"] for seg in result["segments"])

    with open(transcript_json, "w", encoding="utf-8") as f:
        json.dump({
            "full_text": full_text,
            "segments": result["segments"]
        }, f, indent=4)

    # -------- SPEECH REGIONS --------
    spoken_regions = [
        (seg["start"], seg["end"])
        for seg in result["segments"]
        if seg["text"].strip()
    ]

    def overlaps_speech(start, end):
        return any(start < e and end > s for s, e in spoken_regions)

    # -------- VAD --------
    vad = webrtcvad.Vad(2)
    frame_ms = 30
    frame_len = int(sr * frame_ms / 1000)

    def is_voiced(frame):
        pcm = (frame * 32767).astype(np.int16).tobytes()
        return vad.is_speech(pcm, sr)

    # -------- FIND FILLERS --------
    candidates = []
    t = 0
    while t + frame_len < len(y):
        frame = y[t:t + frame_len]
        start = t / sr
        end = (t + frame_len) / sr

        if is_voiced(frame) and not overlaps_speech(start, end):
            candidates.append((start, end))

        t += frame_len

    # -------- MERGE --------
    merged = []
    for seg in candidates:
        if not merged or seg[0] - merged[-1][1] > 0.3:
            merged.append(list(seg))
        else:
            merged[-1][1] = seg[1]

    # -------- FILTER --------
    fillers = []
    for s, e in merged:
        dur = e - s
        if 0.2 <= dur <= 1.5:
            fillers.append({
                "start": round(s, 2),
                "end": round(e, 2),
                "duration": round(dur, 2)
            })

    with open(filler_json, "w") as f:
        json.dump({
            "total_fillers": len(fillers),
            "fillers": fillers
        }, f, indent=4)

    print("✅ Filler + Transcript complete")

    return transcript_json, audio_duration_sec
