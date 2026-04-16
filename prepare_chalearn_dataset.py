import pandas as pd
import os
import numpy as np

# Load the pickle data
data = pd.read_pickle('data/annotations/annotation_training.pkl')

# Create dataframe
videos = list(data['extraversion'].keys())
df = pd.DataFrame({
    'video': videos,
    'extraversion': [data['extraversion'][v] for v in videos],
    'neuroticism': [data['neuroticism'][v] for v in videos],
    'agreeableness': [data['agreeableness'][v] for v in videos],
    'conscientiousness': [data['conscientiousness'][v] for v in videos],
    'openness': [data['openness'][v] for v in videos],
})

print(f"Loaded {len(df)} annotations")
print(df.head())

# Map to public speaking scores (0-100)
df['confidence'] = df['extraversion'] * 100
df['clarity'] = df['conscientiousness'] * 100
df['fluency'] = df['openness'] * 100
df['engagement'] = (df['extraversion'] * 0.6 + df['agreeableness'] * 0.4) * 100
df['nervousness'] = df['neuroticism'] * 100  # Higher neuroticism = more nervous

print("Mapped scores:")
print(df[['video', 'confidence', 'clarity', 'fluency', 'engagement', 'nervousness']].head())

# Filter videos that exist in training80/
video_folder = 'data/training80/'
existing_videos = []
for idx, row in df.iterrows():
    video_path = os.path.join(video_folder, row['video'])
    if os.path.exists(video_path):
        existing_videos.append(row)

df_filtered = pd.DataFrame(existing_videos)
print(f"Found {len(df_filtered)} videos with existing files")

# Save the dataset
df_filtered.to_csv('data/chalearn_dataset.csv', index=False)
print("Saved to data/chalearn_dataset.csv")

# Also save as numpy for training
features = df_filtered[['confidence', 'clarity', 'fluency', 'engagement', 'nervousness']].values
np.save('data/chalearn_scores.npy', features)
video_paths = df_filtered['video'].tolist()
with open('data/chalearn_videos.txt', 'w') as f:
    f.write('\n'.join(video_paths))

print("Saved scores to data/chalearn_scores.npy and video list to data/chalearn_videos.txt")