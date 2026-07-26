import json
from collections import Counter

INPUT = "outputs/failure_analysis.json"
OUTPUT = "outputs/failure_summary.json"

with open(INPUT, "r", encoding="utf-8") as f:
    results = json.load(f)

summary = {
    "base": Counter(),
    "qlora": Counter(),
}

for sample in results:

    for model in ["base", "qlora"]:

        category = sample[model]["failure_diagnosis"]["category"]

        summary[model][category] += 1

summary = {
    model: dict(counter)
    for model, counter in summary.items()
}

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(
        summary,
        f,
        indent=2,
        ensure_ascii=False,
    )

print(json.dumps(summary, indent=2))