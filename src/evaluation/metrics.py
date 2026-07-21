import json
from statistics import mean


RESULTS_PATH = "outputs/evaluation_results.json"
SUMMARY_PATH = "outputs/evaluation_summary.json"



with open(
    RESULTS_PATH,
    "r",
    encoding="utf-8",
) as f:

    results = json.load(f)



metrics = {

    "base": {

        "latency": [],
        "output_tokens": [],
        "words": [],
        "characters": [],
    },

    "qlora": {

        "latency": [],
        "output_tokens": [],
        "words": [],
        "characters": [],
    },
}

for sample in results:

    for model in ["base", "qlora"]:

        result = sample[model]

        metrics[model]["latency"].append(
            result["latency"]
        )

        metrics[model]["output_tokens"].append(
            result["output_tokens"]
        )

        metrics[model]["words"].append(
            result["words"]
        )

        metrics[model]["characters"].append(
            result["characters"]
        )

summary = {}


for model in metrics:

    summary[model] = {

        "average_latency": round(
            mean(metrics[model]["latency"]),
            3,
        ),

        "average_output_tokens": round(
            mean(metrics[model]["output_tokens"]),
            2,
        ),

        "average_words": round(
            mean(metrics[model]["words"]),
            2,
        ),

        "average_characters": round(
            mean(metrics[model]["characters"]),
            2,
        ),
    }

with open(
    SUMMARY_PATH,
    "w",
    encoding="utf-8",
) as f:

    json.dump(
        summary,
        f,
        indent=2,
        ensure_ascii=False,
    )

print()

for model, values in summary.items():

    print(model.upper())

    for key, value in values.items():

        print(f"{key}: {value}")

    print()