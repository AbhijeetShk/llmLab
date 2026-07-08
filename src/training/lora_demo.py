import torch
import torch.nn as nn

in_features = 768
out_features = 768

W = torch.randn(out_features, in_features)

rank = 8

A = torch.randn(rank, in_features)
B = torch.randn(out_features, rank)

delta_W = B @ A

print("Original:", W.shape)
print("LoRA update:", delta_W.shape)

print(
    "Full params:",
    W.numel()
)

print(
    "LoRA params:",
    A.numel() + B.numel()
)