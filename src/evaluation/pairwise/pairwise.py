import json

from tqdm import tqdm

from judges.pairwise_judge import compare


INPUT = "outputs/evaluation_results.json"

OUTPUT = "outputs/pairwise_results.json"


with open(INPUT, "r", encoding="utf-8") as f:
    results = json.load(f)

pairwise = []

for sample in tqdm(results):

    base = sample["base"]["response"]
    qlora = sample["qlora"]["response"]

    forward = compare(
        sample["instruction"],
        sample["reference"],
        base,
        qlora,
    )

    reverse = compare(
        sample["instruction"],
        sample["reference"],
        qlora,
        base,
    )

    if (
        forward["winner"] == "A"
        and reverse["winner"] == "B"
    ):
        winner = "base"

    elif (
        forward["winner"] == "B"
        and reverse["winner"] == "A"
    ):
        winner = "qlora"

    else:
        winner = "tie"

    pairwise.append(
        {
            "instruction": sample["instruction"],
            "winner": winner,
            "forward": forward,
            "reverse": reverse,
            "base": base,
            "qlora": qlora,
        }
    )

with open(
    OUTPUT,
    "w",
    encoding="utf-8",
) as f:

    json.dump(
        pairwise,
        f,
        indent=2,
        ensure_ascii=False,
    )

print("Pairwise evaluation complete.")