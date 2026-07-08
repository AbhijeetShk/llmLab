# LoRA Observations

LoRA freezes original weights.

Instead of updating W directly:

W + BA

Only A and B are trainable.

- Less VRAM
- Faster training
- Smaller checkpoints