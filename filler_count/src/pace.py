import json
from nltk.tokenize import word_tokenize

def pace_features(transcript_json, audio_duration_sec):
    with open(transcript_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    total_words = sum(len(word_tokenize(seg["text"])) for seg in data["segments"])
    spoken_time = sum(seg["end"] - seg["start"] for seg in data["segments"])

    speaking_minutes = spoken_time / 60
    words_per_minute = total_words / max(speaking_minutes, 1)

    return {"words_per_minute": words_per_minute}
