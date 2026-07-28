from dataclasses import dataclass
import torch

from .request import Request


@dataclass
class GenerationState:
    request: Request
    last_token: torch.Tensor | None = None