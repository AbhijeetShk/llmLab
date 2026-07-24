import json

INPUT = "outputs/pairwise_results.json"

with open(INPUT, "r", encoding="utf-8") as f:
    results = json.load(f)

summary = {
    "base": 0,
    "qlora": 0,
    "tie": 0,
}

for r in results:
    summary[r["winner"]] += 1

total = len(results)

print()

print("Pairwise Evaluation")
print("--->")

for model in summary:

    print(
        f"{model:<8}"
        f"{summary[model]:>3}"
        f" ({summary[model]/total:.1%})"
    )