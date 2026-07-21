
from models import DEVICE

import torch
import time

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

    start_time = time.perf_counter() #provides the highest precision timer available and is the standard choice for benchmarking code

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=64,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
    )

    latency = time.perf_counter() - start_time

    text = tokenizer.decode(
        output[0],
        skip_special_tokens=True,
    )

    if text.startswith(prompt):
        text = text[len(prompt):].strip()
    
    input_tokens = inputs["input_ids"].shape[1]

    total_tokens = output.shape[1]

    output_tokens = total_tokens - input_tokens
    character_count = len(text)

    word_count = len(text.split())
    return {
    "response": text,
    "latency": round(latency, 3),
    "input_tokens": input_tokens,
    "output_tokens": output_tokens,
    "total_tokens": total_tokens,
    "characters": character_count,
    "words": word_count,
}