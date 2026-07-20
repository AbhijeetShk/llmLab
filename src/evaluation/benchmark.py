import json

from tqdm import tqdm

from dataset import load_dataset
from inference import generate
from models import (
    load_base,
    load_lora,
)

ADAPTER = "outputs/qlora_adapter"

OUTPUT = "outputs/evaluation_results.json"


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

    question = sample["instruction"]
    reference = sample["response"]

    row = {

        "question": question,

        "reference": reference,
    }

    for name, (
        tokenizer,
        model,
    ) in models.items():

        row[name] = generate(
            model,
            tokenizer,
            question,
        )

    results.append(row)


with open(
    OUTPUT,
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