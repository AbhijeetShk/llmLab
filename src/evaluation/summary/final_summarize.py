import json
from pathlib import Path

OUTPUT_DIR = Path("outputs")

AUTO_METRICS = OUTPUT_DIR / "evaluation_summary.json"
JUDGE_RESULTS = OUTPUT_DIR / "judge_results.json"
PAIRWISE_RESULTS = OUTPUT_DIR / "pairwise_results.json"

FINAL_OUTPUT = OUTPUT_DIR / "final_evaluation_summary.json"


def average(values):
    return sum(values) / len(values) if values else 0



# Automatic Metrics


with open(AUTO_METRICS, "r", encoding="utf-8") as f:
    automatic = json.load(f)



# Judge Metrics


with open(JUDGE_RESULTS, "r", encoding="utf-8") as f:
    judge = json.load(f)


judge_summary = {}

for model in ["base", "qlora"]:

    correctness = []
    completeness = []
    faithfulness = []
    helpfulness = []
    overall = []

    for sample in judge:

        evaluation = sample[model]["evaluation"]

        correctness.append(evaluation["correctness"])
        completeness.append(evaluation["completeness"])
        faithfulness.append(evaluation["faithfulness"])
        helpfulness.append(evaluation["helpfulness"])
        overall.append(evaluation["overall"])

    judge_summary[model] = {
        "correctness": average(correctness),
        "completeness": average(completeness),
        "faithfulness": average(faithfulness),
        "helpfulness": average(helpfulness),
        "overall": average(overall),
    }



# Pairwise


with open(PAIRWISE_RESULTS, "r", encoding="utf-8") as f:
    pairwise = json.load(f)

pairwise_summary = {
    "base": 0,
    "qlora": 0,
    "tie": 0,
}

for sample in pairwise:
    pairwise_summary[sample["winner"]] += 1

total = len(pairwise)

pairwise_summary = {
    **pairwise_summary,
    "base_win_rate": pairwise_summary["base"] / total,
    "qlora_win_rate": pairwise_summary["qlora"] / total,
    "tie_rate": pairwise_summary["tie"] / total,
}



# Final


final = {
    "automatic_metrics": automatic,
    "llm_judge": judge_summary,
    "pairwise": pairwise_summary,
}

with open(FINAL_OUTPUT, "w", encoding="utf-8") as f:
    json.dump(
        final,
        f,
        indent=2,
        ensure_ascii=False,
    )

print("Final evaluation summary generated.")