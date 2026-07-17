import time
import torch

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
)

MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME
)

model.eval()

prompt = "Explain Retrieval Augmented Generation."

inputs = tokenizer(
    prompt,
    return_tensors="pt"
)


# Trying without cache


start = time.time()

_ = model.generate(
    **inputs,
    max_new_tokens=100,
    use_cache=False,
)

without_cache = time.time() - start

# Using Cache below

start = time.time()

_ = model.generate(
    **inputs,
    max_new_tokens=100,
    use_cache=True,
)

with_cache = time.time() - start

print()

print(f"Without Cache: {without_cache:.2f}s")
print(f"With Cache:    {with_cache:.2f}s")

print(
    f"Speedup: {without_cache / with_cache:.2f}x"
)