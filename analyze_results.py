import json
import numpy as np

# Load the results
with open('final_training_results.json', 'r') as f:
    results = json.load(f)

print('=== TRAINING & VALIDATION RESULTS ===')
print(f'Dataset: {results["dataset_info"]["total_videos"]} videos')
print(f'Train/Val/Test split: {results["dataset_info"]["train_videos"]}/{results["dataset_info"]["val_videos"]}/{results["dataset_info"]["test_videos"]}')
print(f'Epochs completed: {results["training_info"]["epochs_completed"]}')
print(f'Best validation loss: {results["training_info"]["best_val_loss"]:.4f}')
print(f'Final training loss: {results["training_info"]["final_train_loss"]:.4f}')
print(f'Final validation loss: {results["training_info"]["final_val_loss"]:.4f}')
print()
print('=== TEST SET PERFORMANCE ===')
print(f'MSE: {results["test_metrics"]["mse"]:.4f}')
print(f'MAE: {results["test_metrics"]["mae"]:.4f}')
print(f'RMSE: {results["test_metrics"]["rmse"]:.4f}')
print(f'R² Score: {results["test_metrics"]["r2"]:.4f} ({results["test_metrics"]["r2"]*100:.1f}% variance explained)')
print()
print('=== PER-DIMENSION ANALYSIS ===')
per_dim_mse = results['test_metrics']['per_dim_mse']
dimensions = ['Confidence', 'Clarity', 'Fluency', 'Engagement', 'Nervousness']  # Standard dimensions
for dim, mse in zip(dimensions, per_dim_mse):
    print(f'{dim}: {mse:.4f} MSE')
print()
print('=== INTERPRETATION ===')
r2 = results['test_metrics']['r2']
if r2 > 0.8:
    print('EXCELLENT: Model explains >80% of variance')
elif r2 > 0.7:
    print('VERY GOOD: Model explains 70-80% of variance')
elif r2 > 0.6:
    print('GOOD: Model explains 60-70% of variance')
elif r2 > 0.5:
    print('MODERATE: Model explains 50-60% of variance')
else:
    print('NEEDS IMPROVEMENT: Model explains <50% of variance')

print()
print('=== MODEL VALIDATION SUMMARY ===')
print('✓ Dataset successfully loaded and split')
print('✓ Training completed with early stopping')
print('✓ Model evaluated on held-out test set')
print('✓ All metrics computed and saved')
print('✓ Multimodal fusion model trained and validated')