import torch

from transformers import (
    AutoModelForCausalLM,
)

MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME
)

weights = []

for p in model.parameters():

    weights.append(
        p.detach().flatten()
    )

weights = torch.cat(weights)

print("Min:", weights.min().item())
print("Max:", weights.max().item())
print("Mean:", weights.mean().item())
print("Std:", weights.std().item())