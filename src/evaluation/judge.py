import json

from tqdm import tqdm

from judges.groq_judge import judge_response


INPUT = "outputs/evaluation_results.json"

OUTPUT = "outputs/judge_results.json"


with open(
    INPUT,
    "r",
    encoding="utf-8",
) as f:

    results = json.load(f)


judged = []


for sample in tqdm(results):

    row = {

        "instruction": sample["instruction"],

        "reference": sample["reference"],
    }

    for model in ["base", "qlora"]:

        prediction = sample[model]["response"]

        evaluation = judge_response(
            sample["instruction"],
            sample["reference"],
            prediction,
        )

        row[model] = {
            "response": prediction,
            "evaluation": evaluation,
        }

    judged.append(row)


with open(
    OUTPUT,
    "w",
    encoding="utf-8",
) as f:

    json.dump(
        judged,
        f,
        indent=2,
        ensure_ascii=False,
    )

print("Judge evaluation complete.")