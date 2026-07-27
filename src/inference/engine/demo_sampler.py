import torch

from .sampler import Sampler


logits = torch.randn(
    1,
    100,
)

print("-->")
print("Greedy")
print(
    Sampler.greedy(logits)
)

print("-->")
print("Temperature")
print(
    Sampler.temperature(
        logits,
        temperature=0.8,
    )
)

print("-->")
print("Top-K")
print(
    Sampler.top_k(
        logits,
        k=10,
    )
)

print("-->")
print("Top-P")
print(
    Sampler.top_p(
        logits,
        p=0.9,
    )
)