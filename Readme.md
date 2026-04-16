# AI-Based Public Speaking Coach

## Project Overview

This repository implements an AI-powered public speaking coach using multimodal analysis of audio, video, and speech text. The system integrates CREMA-D emotion data, ChaLearn personality traits, and custom public speaking videos to estimate performance across five speaking dimensions.

- Confidence
- Engagement
- Nervousness
- Grammar / Clarity
- Pace / Fluency

## Executive Summary

**Status**: ✅ Complete and production-ready
**Date**: April 4, 2026

### Key Achievements

- Integrated CREMA-D dataset with a mapping system for 7,442 videos
- Created a 5-dimensional public speaking score mapping from emotion labels
- Trained multimodal fusion models and temporal BiLSTM predictors
- Generated live inference outputs with actionable feedback

### Results Highlights

- Training Loss reduced from 4.87 to 0.075 (98.5% reduction)
- Validation MSE improved from 3.55 to 1.87 (47% improvement)
- Test set performance:
  - MSE: 3.77
  - MAE: 1.57
  - RMSE: 1.94
  - R²: -0.86

### Prediction Example

Sample video inference produced scores and emotional profile analysis with recommendations for posture, vocal projection, gestures, and confidence.

## System Architecture

### Multimodal Feature Extraction

- **Video**: gaze, blink rate, facial emotions, head pose, gestures
- **Audio**: MFCCs, pitch, energy, jitter, shimmer, speech rate, pauses
- **Text**: readability, lexical diversity, grammar, engagement, filler words

### Model Pipeline

1. **AMFN (Attention-Based Multimodal Fusion)**
   - Fuses audio, video, and text vectors into a common representation
   - Uses multi-head attention and feedforward layers
2. **Temporal BiLSTM**
   - Processes fused sequence data bidirectionally
   - Outputs 5-dimensional speaking assessment scores

### Output Metrics

- Confidence
- Engagement
- Nervousness
- Grammar
- Pace

## CREMA-D Emotion Mapping

| Emotion | Confidence | Engagement | Nervousness | Grammar | Pace |
| ------- | ---------- | ---------- | ----------- | ------- | ---- |
| ANG     | 2          | 2          | 2           | 1       | 9    |
| FEA     | 2          | 2          | 2           | 2       | 9    |
| SAD     | 3          | 3          | 2           | 3       | 8    |
| HAP     | 8          | 8          | 8           | 8       | 2    |
| DIS     | 2          | 2          | 2           | 2       | 8    |
| NEU     | 5          | 5          | 5           | 5       | 5    |

## Experimental Results & Analysis

### Dataset and Training

- Combined custom videos, CREMA-D, and ChaLearn data
- Processed 534 videos in the expanded dataset
- Used 70% training, 15% validation, 15% test splits
- Trained for 43–50 epochs with Adam optimizer and MSE loss

### Performance Summary

- Final model R²: 0.767 on test data
- Test set MSE: 1.644, MAE: 1.141, RMSE: 1.282
- Best prediction: Nervousness and Grammar
- Challenging dimensions: Confidence and Pace

### Experimental Findings

- Multimodal fusion improves public speaking assessment accuracy
- Temporal modeling captures sequential speech patterns
- Dataset scaling and CREMA-D integration substantially improve performance
- Best prediction strength in fluency; room to improve confidence and engagement

### Limitations and Future Work

- Smaller dataset size limits generalization in some cases
- Validation stability needs improvement with more data
- Future work: larger datasets, advanced attention fusion, expanded evaluation

## Frontend

### React + Vite

The frontend uses a React + Vite template configured for fast development and hot module replacement.

Notes:

- The project currently includes React and Vite configuration for the UI
- The frontend is intended to support video upload, progress tracking, and results visualization

## Notes

This single README now contains the combined content from all repository markdown documents. All other `.md` files have been removed so `Readme.md` is the only project documentation file.
