import os
import json
import re
from transformers import pipeline

# ---------------- CONFIG ----------------
MODEL_NAME = "SamLowe/roberta-base-go_emotions"
MAX_SENTENCE_CHARS = 350

# ---------------- TEXT HELPERS ----------------
def clean_text(text):
    """Remove filler words and normalize spacing"""
    fillers = [
        r"\bum+\b", r"\buh+\b", r"\bah+\b", r"\ber+\b", r"\bhmm+\b"
    ]
    for f in fillers:
        text = re.sub(f, "", text, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", text).strip()


def split_sentences(text):
    sentences = re.split(r"(?<=[.!?])\s+", text)
    return [s.strip() for s in sentences if len(s.strip()) > 5]


# ---------------- MAIN PIPELINE ----------------

def run_emotion_pipeline(transcript_json, output_dir):
    emotion_out = os.path.join(output_dir, "emotion_report.json")
    with open(transcript_json, "r", encoding="utf-8") as f:
        transcript = json.load(f)
    text = transcript["full_text"]

    classifier = pipeline("text-classification", model=MODEL_NAME, top_k=None)
    results = classifier(text[:512])[0]  # first 512 chars for simplicity

    # Take top 5 emotions
    top_emotions = sorted(results, key=lambda x: x['score'], reverse=True)[:5]
    emotion_vector = [e['score'] for e in top_emotions]

    # Save JSON
    with open(emotion_out, "w") as f:
        json.dump({"emotions": top_emotions}, f, indent=4)

    return {"emotion_vector": emotion_vector}
