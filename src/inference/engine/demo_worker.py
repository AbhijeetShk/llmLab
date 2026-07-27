import torch

from .worker import ModelWorker


MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

worker = ModelWorker(MODEL_NAME)

prompt = "Explain LoRA in one sentence."

#Encode

input_ids = worker.encode(prompt)

print("-->")
print("INPUT IDS")
print(input_ids)

#prefill

logits, cache = worker.prefill(input_ids)

print("-->")
print("LOGITS SHAPE")
print(logits.shape)

#Greedy next token

next_token = torch.argmax(
    logits,
    dim=-1,
    keepdim=True,
)

print("-->")
print("NEXT TOKEN")
print(next_token)

#decode token

text = worker.decode_tokens(
    next_token.squeeze()
)

print("-->")
print("TOKEN")
print(text)