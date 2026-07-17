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

prompt = "What is Retrieval Augmented Generation?"

input_ids = tokenizer.encode(
    prompt,
    return_tensors="pt"
)

generated = input_ids

past_key_values = None

max_new_tokens = 50

for step in range(max_new_tokens):

    with torch.no_grad():

        outputs = model(
            input_ids=generated[:, -1:]
            if past_key_values is not None
            else generated,
            past_key_values=past_key_values,
            use_cache=True,
        )

    logits = outputs.logits

    past_key_values = outputs.past_key_values

    next_token = torch.argmax(
        logits[:, -1, :],
        dim=-1,
        keepdim=True,
    )

    generated = torch.cat(
        [generated, next_token],
        dim=1,
    )

    token = tokenizer.decode(
        next_token[0]
    )

    print(
        f"Step {step+1}: {token}"
    )

print("\n" + "=" * 80)

print(
    tokenizer.decode(
        generated[0],
        skip_special_tokens=True,
    )
)