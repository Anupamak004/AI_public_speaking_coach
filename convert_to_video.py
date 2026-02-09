# convert_cremad_videos.py
import os
import subprocess

SRC = "data/crema-d/VideoFlash"
DST = "data/crema-d/VideoMP4"
os.makedirs(DST, exist_ok=True)

for file in os.listdir(SRC):
    if file.endswith(".flv"):
        in_file = os.path.join(SRC, file)
        out_file = os.path.join(DST, file.replace(".flv", ".mp4"))

        if not os.path.exists(out_file):
            subprocess.run([
                "ffmpeg", "-y", "-i", in_file,
                "-movflags", "faststart",
                "-pix_fmt", "yuv420p",
                out_file
            ])

print("✅ CREMA-D videos converted to MP4")
