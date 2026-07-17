import torch

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
)

MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME)

prompt = "The capital of France is"

inputs = tokenizer(
    prompt,
    return_tensors="pt"
)

with torch.no_grad():

    outputs = model(**inputs)

logits = outputs.logits

last_logits = logits[:, -1, :]

probs = torch.softmax(
    last_logits,
    dim=-1,
)

top_probs, top_indices = torch.topk(
    probs,
    k=10,
)

print("\nTop Predictions:\n")

for p, idx in zip(
    top_probs[0],
    top_indices[0],
):
    token = tokenizer.decode(
        idx
    )

    print(
        f"{token!r:<15} {p.item():.4f}"
    )