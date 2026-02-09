import os
import json
import numpy as np

from .hybrid_filler_count import run_filler_pipeline
from .emotion_analysis import run_emotion_pipeline
from .readability import readability_features
from .vocabulary import vocabulary_features
from .confidence import confidence_features
from .grammar import grammar_features
from .engagement import engagement_features
from .pace import pace_features


def run_text_pipeline(video_path, output_dir="outputs"):
    os.makedirs(output_dir, exist_ok=True)

    # ---------- STEP 1: TRANSCRIPTION + FILLERS ----------
    transcript_path, audio_duration, filler_json = run_filler_pipeline(
        video_path, output_dir
    )

    # ---------- LOAD FILLER COUNT ----------
    with open(filler_json, "r") as f:
        filler_data = json.load(f)
    filler_count = filler_data.get("total_fillers", 0)

    # ---------- STEP 2: EMOTION ANALYSIS ----------
    run_emotion_pipeline(transcript_path, output_dir)

    # ---------- STEP 3: TEXT-BASED ANALYSIS ----------
    with open(transcript_path, "r", encoding="utf-8") as f:
        transcript = json.load(f)

    text = transcript["full_text"]

    readability = readability_features(text)
    vocabulary = vocabulary_features(text)
    confidence = confidence_features(text)
    grammar = grammar_features(text)
    engagement = engagement_features(text)
    pace = pace_features(transcript_path, audio_duration)

    # ---------- MERGE ALL FEATURES (UNCHANGED) ----------
    text_vector = np.array([
        readability["readability_score"],
        vocabulary["lexical_diversity"],
        confidence["confidence_score"],
        grammar["grammar_error_rate"],
        engagement["engagement_score"],
        pace["words_per_minute"],
        filler_count
    ])

    # ---------- SAVE ALL STATS (UNCHANGED) ----------
    text_stats = {
        **readability,
        **vocabulary,
        **confidence,
        **grammar,
        **engagement,
        **pace,
        "filler_count": filler_count
    }

    with open(
        os.path.join(output_dir, "text_features.json"),
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(text_stats, f, indent=4)

    # ---------- RETURN ONLY ESSENTIAL FEATURES TO FUSION ----------
    essential_text_vector = np.array([
        readability["readability_score"],
        vocabulary["lexical_diversity"],
        grammar["grammar_error_rate"],
        pace["words_per_minute"],
        filler_count
    ])

    return {
        "text_vector": essential_text_vector,   # ✅ ONLY THIS GOES TO FUSION
        "text_stats": text_stats,               # kept for reports/UI
        "transcript_path": transcript_path,
        "audio_duration": audio_duration
    }
