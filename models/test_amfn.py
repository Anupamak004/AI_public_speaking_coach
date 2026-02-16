import torch
from amfn import AMFN

model = AMFN(audio_dim=21, video_dim=64, text_dim=5)

audio = torch.rand(1, 21)
video = torch.rand(1, 64)
text  = torch.rand(1, 5)

out = model(audio, video, text)

print("Fusion output shape:", out.shape)
