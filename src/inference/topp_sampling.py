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

prompt = "Explain machine learning."

inputs = tokenizer(
    prompt,
    return_tensors="pt"
)

for top_p in [0.5, 0.8, 0.9, 0.95]:


    print(f"Top-P = {top_p}")


    output = model.generate(
        **inputs,
        max_new_tokens=100,
        do_sample=True,
        top_p=top_p,
    )

    print(
        tokenizer.decode(
            output[0],
            skip_special_tokens=True,
        )
    )