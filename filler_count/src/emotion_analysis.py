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

    # -------- LOAD TRANSCRIPT --------
    with open(transcript_json, "r", encoding="utf-8") as f:
        transcript = json.load(f)

    raw_text = transcript["full_text"]
    clean = clean_text(raw_text)
    sentences = split_sentences(clean)

    print(f"🧠 Analysing emotion from {len(sentences)} sentences")

    # -------- LOAD MODEL --------
    classifier = pipeline(
        "text-classification",
        model=MODEL_NAME,
        top_k=None
    )

    emotion_totals = {}
    total_weight = 0

    # -------- SENTENCE-LEVEL EMOTION --------
    for sentence in sentences:
        if len(sentence) > MAX_SENTENCE_CHARS:
            continue

        results = classifier(sentence)[0]
        weight = len(sentence)
        total_weight += weight

        for r in results:
            emotion_totals[r["label"]] = (
                emotion_totals.get(r["label"], 0) + r["score"] * weight
            )

    # -------- NORMALIZE --------
    final_emotions = [
        {"label": k, "score": round(v / total_weight, 4)}
        for k, v in emotion_totals.items()
    ]
    final_emotions.sort(key=lambda x: x["score"], reverse=True)

    # -------- SAVE --------
    with open(emotion_out, "w", encoding="utf-8") as f:
        json.dump(
            {
                "text_length": len(raw_text),
                "sentences_used": len(sentences),
                "emotions": final_emotions
            },
            f,
            indent=4
        )

    print("✅ Emotion analysis complete")
    for e in final_emotions[:5]:
        print(f"{e['label']}: {e['score']}")
