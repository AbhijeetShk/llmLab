import json


with open(
    "outputs/evaluation_results.json",
    "r",
    encoding="utf-8",
) as f:

    results = json.load(f)


lines = []

lines.append("-> QLoRA Evaluation Report\n")


for i, sample in enumerate(results):

    lines.append(f"-> Sample {i+1}\n")

    lines.append(
        f"-> Question\n{sample['question']}\n"
    )

    lines.append(
        f"-> Reference\n{sample['reference']}\n"
    )

    lines.append(
        f"-> Base\n{sample['base']}\n"
    )

    lines.append(
        f"-> QLoRA\n{sample['qlora']}\n"
    )

    lines.append("---\n")


with open(
    "outputs/evaluation_report.md",
    "w",
    encoding="utf-8",
) as f:

    f.write(
        "\n".join(lines)
    )

print("Report generated.")