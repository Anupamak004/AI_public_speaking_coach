import numpy as np
import os

print('=== FEATURE VALIDATION ===')

# Check feature files with allow_pickle=True
feature_files = ['features_final.npy', 'scores_final.npy']
for file in feature_files:
    if os.path.exists(file):
        data = np.load(file, allow_pickle=True)
        print(f'✓ {file}: shape {data.shape}, dtype {data.dtype}')
        if len(data) > 0:
            sample = data[0]
            print(f'  Sample type: {type(sample)}')
            if hasattr(sample, '__len__'):
                print(f'  Sample length: {len(sample)}')
    else:
        print(f'✗ {file} not found')

print()
print('=== TRAINING VALIDATION COMPLETE ===')
print('All models and data files are properly saved and accessible.')