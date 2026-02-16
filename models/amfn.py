import torch
import torch.nn as nn


class AMFN(nn.Module):
    """
    Attention-Based Multimodal Fusion Network
    """

    def __init__(
        self,
        audio_dim,
        video_dim,
        text_dim,
        latent_dim=128,
        num_heads=4
    ):
        super().__init__()

        # -------- Projection Layers --------
        self.audio_proj = nn.Linear(audio_dim, latent_dim)
        self.video_proj = nn.Linear(video_dim, latent_dim)
        self.text_proj  = nn.Linear(text_dim, latent_dim)

        # -------- Multi-Head Attention --------
        self.attention = nn.MultiheadAttention(
            embed_dim=latent_dim,
            num_heads=num_heads,
            batch_first=True
        )

        # -------- Feed Forward Refinement --------
        self.ffn = nn.Sequential(
            nn.Linear(latent_dim, latent_dim),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(latent_dim, latent_dim)
        )

        self.norm1 = nn.LayerNorm(latent_dim)
        self.norm2 = nn.LayerNorm(latent_dim)

    def forward(self, audio_vec, video_vec, text_vec):
        """
        audio_vec: (B, A)
        video_vec: (B, V)
        text_vec : (B, T)
        """

        # ---- Project to Common Space ----
        audio = self.audio_proj(audio_vec)
        video = self.video_proj(video_vec)
        text  = self.text_proj(text_vec)

        # ---- Stack Modalities ----
        # Shape: (B, 3, latent_dim)
        multimodal = torch.stack([audio, video, text], dim=1)

        # ---- Attention ----
        attn_out, _ = self.attention(
            multimodal,
            multimodal,
            multimodal
        )

        x = self.norm1(multimodal + attn_out)

        # ---- Feed Forward ----
        ffn_out = self.ffn(x)
        x = self.norm2(x + ffn_out)

        # ---- Final Fusion Vector ----
        # Mean pooling across modalities
        fusion_vector = x.mean(dim=1)

        return fusion_vector
