import math
from moviepy import VideoFileClip


def get_video_duration(video_path):
    """Returns duration of video in seconds (float)"""
    clip = VideoFileClip(video_path)
    duration = clip.duration
    clip.close()
    return duration


def segment_video(video_path, window_size=5):
    duration_sec = float(get_video_duration(video_path))

    segments = []
    num_segments = math.ceil(duration_sec / window_size)

    for i in range(num_segments):
        start = i * window_size
        end = min(start + window_size, duration_sec)
        segments.append((start, end))

    return segments

