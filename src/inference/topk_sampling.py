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

prompt = "Tell me about artificial intelligence."

inputs = tokenizer(
    prompt,
    return_tensors="pt"
)

for top_k in [5, 20, 50, 100]:


    print(f"Top-K = {top_k}")


    output = model.generate(
        **inputs,
        max_new_tokens=100,
        do_sample=True,
        top_k=top_k,
    )

    print(
        tokenizer.decode(
            output[0],
            skip_special_tokens=True,
        )
    )