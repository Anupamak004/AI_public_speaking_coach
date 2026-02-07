import os
import json

from hybrid_filler_count import run_filler_pipeline
from emotion_analysis import run_emotion_pipeline

from readability import readability_features
from vocabulary import vocabulary_features
from confidence import confidence_features
from grammar import grammar_features
from engagement import engagement_features
from pace import pace_features

# ---------------- PATHS ----------------
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIDEO = os.path.join(ROOT, "data", "video", "sample_video1.mp4")
OUTPUT = os.path.join(ROOT, "outputs")
TRANSCRIPT_JSON = os.path.join(OUTPUT, "transcript.json")

print("\n🚀 RUNNING FULL PUBLIC SPEAKING PIPELINE\n")

# ---------- STEP 1: TRANSCRIPTION + FILLERS ----------
transcript_path, audio_duration = run_filler_pipeline(VIDEO, OUTPUT)

# ---------- STEP 2: EMOTION ANALYSIS ----------
run_emotion_pipeline(transcript_path, OUTPUT)

# ---------- STEP 3: TEXT-BASED ANALYSIS ----------
print("\n📊 PUBLIC SPEAKING TEXT ANALYSIS\n")

with open(transcript_path, "r", encoding="utf-8") as f:
    transcript = json.load(f)

text = transcript["full_text"]

readability_features(text)
vocabulary_features(text)
confidence_features(text)
grammar_features(text)
engagement_features(text)

# ---------- STEP 4: PACE (uses timestamps) ----------
pace_features(transcript_path, audio_duration)

print("\n🎉 ALL ANALYSIS COMPLETE\n")
