import json
import nltk
from nltk.tokenize import word_tokenize

def pace_features(transcript_json, audio_duration_sec):
    print("🔹 Speaking Pace Analysis")

    with open(transcript_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    total_words = 0
    spoken_time = 0.0  # seconds

    for seg in data["segments"]:
        text = seg["text"].strip()
        if text:
            total_words += len(word_tokenize(text))
            spoken_time += (seg["end"] - seg["start"])

    # Convert seconds → minutes
    speaking_minutes = spoken_time / 60
    total_minutes = audio_duration_sec / 60

    speaking_wpm = total_words / speaking_minutes if speaking_minutes > 0 else 0
    delivery_wpm = total_words / total_minutes if total_minutes > 0 else 0

    print("Total Words:", total_words)
    print("Speaking Time (sec):", round(spoken_time, 2))
    print("Total Duration (sec):", round(audio_duration_sec, 2))
    print("Audio Duration :", audio_duration_sec)

    print("\n🗣 Speaking Pace (no silence):", round(speaking_wpm, 2), "WPM")
    print("🎬 Delivery Pace (with silence):", round(delivery_wpm, 2), "WPM")

    # Feedback
    if speaking_wpm < 130:
        print("⚠ Speaking too slowly")
    elif speaking_wpm > 170:
        print("⚠ Speaking too fast")
    else:
        print("✅ Speaking pace is ideal")

    if delivery_wpm < 100:
        print("⚠ Too many pauses / low engagement")
    elif delivery_wpm > 150:
        print("⚠ Very dense speech")
    else:
        print("✅ Good overall delivery flow")
