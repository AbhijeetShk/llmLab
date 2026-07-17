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

generated = input_ids.clone()

max_new_tokens = 50

for step in range(max_new_tokens):

    with torch.no_grad():

        outputs = model(
            generated
        )

    logits = outputs.logits

    next_token_logits = logits[:, -1, :]

    next_token = torch.argmax(
        next_token_logits,
        dim=-1,
        keepdim=True,
    )

    generated = torch.cat(
        [generated, next_token],
        dim=1,
    )

    decoded = tokenizer.decode(
        next_token[0]
    )

    print(
        f"Step {step + 1}: {decoded}"
    )

result = tokenizer.decode(
    generated[0],
    skip_special_tokens=True,
)

print("\n" + "=" * 80)
print(result)