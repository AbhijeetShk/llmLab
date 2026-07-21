import json

from tqdm import tqdm

from dataset import load_dataset
from inference import generate
from models import (
    load_base,
    load_lora,
)

ADAPTER = "outputs/qlora_adapter"

RESULTS_PATH = "outputs/evaluation_results.json"


print("Loading models...")

base_tok, base_model = load_base()

lora_tok, lora_model = load_lora(
    ADAPTER
)

models = {

    "base": (
        base_tok,
        base_model,
    ),

    "qlora": (
        lora_tok,
        lora_model,
    ),
}


dataset = load_dataset(
    "dataset/eval_dataset_structured.json"
)

results = []


for sample in tqdm(dataset):
    instruction = sample["instruction"]
    reference = sample["response"]

    row = {
        "instruction": instruction,
        "reference": reference,
    }

    for name, (
        tokenizer,
        model,
    ) in models.items():

        row[name] = generate(
            model,
            tokenizer,
            instruction,
        )

    results.append(row)


with open(
    RESULTS_PATH,
    "w",
    encoding="utf-8",
) as f:

    json.dump(
        results,
        f,
        indent=2,
        ensure_ascii=False,
    )

print("Finished.")