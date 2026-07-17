import torch

weights = torch.randn(
    10000
)

min_val = weights.min()
max_val = weights.max()

scale = (
    max_val - min_val
) / 255

quantized = (
    (weights - min_val)
    / scale
).round()

dequantized = (
    quantized * scale
    + min_val
)

error = (
    weights - dequantized
).abs()

print(
    "Mean Error:",
    error.mean().item()
)

print(
    "Max Error:",
    error.max().item()
)