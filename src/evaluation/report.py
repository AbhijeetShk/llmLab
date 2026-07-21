import json

REPORT_PATH = "outputs/evaluation_report.md"
RESULTS_PATH = "outputs/evaluation_results.json"
with open(
    RESULTS_PATH,
    "r",
    encoding="utf-8",
) as f:

    results = json.load(f)


lines = []

lines.append("-> QLoRA Evaluation Report\n")


for i, sample in enumerate(results):

    lines.append(f"-> Sample {i + 1}\n")

    lines.append("-> Instruction")
    lines.append(sample["instruction"])
    lines.append("")

    lines.append("-> Reference")
    lines.append(sample["reference"])
    lines.append("")

    for model_name in ["base", "qlora"]:

        result = sample[model_name]

        lines.append(f"-> {model_name.upper()}")

        lines.append(f"- Latency: {result['latency']} s")
        lines.append(f"- Input Tokens: {result['input_tokens']}")
        lines.append(f"- Output Tokens: {result['output_tokens']}")
        lines.append(f"- Total Tokens: {result['total_tokens']}")
        lines.append(f"- Characters: {result['characters']}")
        lines.append(f"- Words: {result['words']}")
        lines.append("")

        lines.append("-> Response")
        lines.append(result["response"])
        lines.append("")

    lines.append("---\n")


with open(
    REPORT_PATH,
    "w",
    encoding="utf-8",
) as f:

    f.write(
        "\n".join(lines)
    )

print("Report generated.")