import torch
import numpy as np
import os
import sys

PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(PATH, "..", "models"))
from models.amfn import AMFN


class MultimodalFusionEngine:
    def __init__(self, audio_dim, video_dim, text_dim):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.model = AMFN(
            audio_dim=audio_dim,
            video_dim=video_dim,
            text_dim=text_dim
        ).to(self.device)

        self.model.eval()  # inference mode

    def fuse(self, audio_vector, video_vector, text_vector):
        """
        Uses feature vectors from your existing pipelines
        """

        audio = torch.tensor(audio_vector, dtype=torch.float32).unsqueeze(0).to(self.device)
        video = torch.tensor(video_vector, dtype=torch.float32).unsqueeze(0).to(self.device)
        text  = torch.tensor(text_vector, dtype=torch.float32).unsqueeze(0).to(self.device)

        with torch.no_grad():
            fusion_vector = self.model(audio, video, text)

        return fusion_vector.cpu().numpy().squeeze()
