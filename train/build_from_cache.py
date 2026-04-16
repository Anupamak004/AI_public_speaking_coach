import os
import numpy as np
import pandas as pd
from pathlib import Path

# Load cached processed videos and create final dataset
def build_dataset_from_cache():
    features_list = []
    scores_list = []

    # Load ChaLearn data
    chalearn_df = pd.read_csv("data/chalearn_dataset.csv")

    # Process cached videos
    cache_dirs = {
        'video_cache': ('data/videos', None),  # Custom videos with predefined scores
        'crema_cache': ('data/crema-d/VideoMP4', None),  # CREMA-D with emotion mapping
        'chalearn_cache': ('data/training80', chalearn_df)  # ChaLearn with CSV mapping
    }

    for cache_dir, (video_base_dir, df) in cache_dirs.items():
        if not os.path.exists(cache_dir):
            continue

        print(f"Loading from {cache_dir}...")

        for cache_file in os.listdir(cache_dir):
            if not cache_file.endswith('_cache.npy'):
                continue

            try:
                cache_path = os.path.join(cache_dir, cache_file)
                data = np.load(cache_path, allow_pickle=True)

                segment_data, score = data

                # Validate data
                if len(segment_data) > 0 and len(score) == 5:
                    features_list.append(segment_data)
                    scores_list.append(np.asarray(score, dtype=np.float32))
                    print(f"  Loaded {cache_file}")

            except Exception as e:
                print(f"  Error loading {cache_file}: {e}")
                continue

    return np.array(features_list, dtype=object), np.array(scores_list, dtype=np.float32)

if __name__ == "__main__":
    print("Building dataset from cached videos...")
    features, scores = build_dataset_from_cache()

    print(f"Dataset built: {len(features)} videos")

    if len(features) > 0:
        np.save("features_final.npy", features)
        np.save("scores_final.npy", scores)
        print("Saved features_final.npy and scores_final.npy")
    else:
        print("No data found!")