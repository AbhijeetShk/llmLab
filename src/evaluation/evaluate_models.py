import json
import torch
from tqdm import tqdm

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
)

from peft import PeftModel


BASE_MODEL = "Qwen/Qwen2.5-1.5B-Instruct"
ADAPTER_PATH = "outputs/qlora_adapter"
OUTPUT_FILE = "outputs/evaluation_results.json"




if torch.backends.mps.is_available():
    DEVICE = torch.device("mps")
elif torch.cuda.is_available():
    DEVICE = torch.device("cuda")
else:
    DEVICE = torch.device("cpu")

print(f"\nUsing device: {DEVICE}\n")




with open(
    "dataset/eval_dataset.json",
    "r",
    encoding="utf-8",
) as f:
    eval_data = json.load(f)




def load_base():
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)

    model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        torch_dtype=torch.float16 if DEVICE.type != "cpu" else torch.float32,
    )

    model.to(DEVICE)
    model.eval()

    return tokenizer, model


def load_lora(adapter_path):
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)

    base = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        torch_dtype=torch.float16 if DEVICE.type != "cpu" else torch.float32,
    )

    model = PeftModel.from_pretrained(
        base,
        adapter_path,
    )

    model.to(DEVICE)
    model.eval()

    return tokenizer, model




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

    generated = tokenizer.decode(
        output[0],
        skip_special_tokens=True,
    )

    
    if generated.startswith(prompt):
        generated = generated[len(prompt):].strip()

    return generated




print("Loading Base Model...")
base_tokenizer, base_model = load_base()

print("Loading QLoRA Model...")
lora_tokenizer, lora_model = load_lora(ADAPTER_PATH)


models = {
    "base": (base_tokenizer, base_model),
    "qlora": (lora_tokenizer, lora_model),
}




results = []

for item in tqdm(eval_data, desc="Evaluating"):

    instruction = item["question"]

    row = {
        "question": instruction,
    }

    for name, (tokenizer, model) in models.items():

        print(f"\n{name.upper()} -> {instruction}")

        answer = generate(
            model,
            tokenizer,
            instruction,
        )

        row[name] = answer

    results.append(row)




with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8",
) as f:
    json.dump(
        results,
        f,
        indent=2,
        ensure_ascii=False,
    )

print("\nEvaluation complete.")
print(f"Saved to: {OUTPUT_FILE}")