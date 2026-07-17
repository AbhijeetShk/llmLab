from transformers import (
    AutoModelForCausalLM,
)

MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME
)

total_params = sum(
    p.numel()
    for p in model.parameters()
)

print(f"Parameters: {total_params:,}")

fp32_memory = total_params * 4 / 1024**3
fp16_memory = total_params * 2 / 1024**3
int8_memory = total_params * 1 / 1024**3
int4_memory = total_params * 0.5 / 1024**3

print(f"FP32 : {fp32_memory:.2f} GB")
print(f"FP16 : {fp16_memory:.2f} GB")
print(f"INT8 : {int8_memory:.2f} GB")
print(f"INT4 : {int4_memory:.2f} GB")