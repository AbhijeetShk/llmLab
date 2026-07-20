from models import DEVICE

import torch


def generate(
    model,
    tokenizer,
    instruction,
):

    prompt = (
        f"-> Instruction:\n"
        f"{instruction}\n\n"
        f"-> Response:\n"
    )

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
    ).to(DEVICE)

    with torch.no_grad():

        output = model.generate(
            **inputs,
            max_new_tokens=64,
            do_sample=False,
            temperature=0.0,
            pad_token_id=tokenizer.eos_token_id,
        )

    text = tokenizer.decode(
        output[0],
        skip_special_tokens=True,
    )

    if text.startswith(prompt):
        text = text[len(prompt):].strip()

    return text