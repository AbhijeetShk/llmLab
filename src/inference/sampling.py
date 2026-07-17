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

for temperature in [0.2, 0.7, 1.0, 1.5]:


    print(f"Temperature = {temperature}")


    output = model.generate(
        **inputs,
        max_new_tokens=80,
        do_sample=True,
        temperature=temperature,
    )

    text = tokenizer.decode(
        output[0],
        skip_special_tokens=True,
    )

    print(text)