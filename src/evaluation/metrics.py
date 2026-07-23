import json
from statistics import mean

from quality import compute_bleu, compute_rouge
from quality import (
    compute_bleu,
    compute_rouge,
    compute_bertscore,
)

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
        "bleu": [],

        "rouge1": [],

        "rouge2": [],

        "rougeL": [],
        "bertscore_precision": [],

        "bertscore_recall": [],

        "bertscore_f1": [],
    },

    "qlora": {

        "latency": [],
        "output_tokens": [],
        "words": [],
        "characters": [],
        "bleu": [],

        "rouge1": [],

        "rouge2": [],

        "rougeL": [],
        "bertscore_precision": [],

        "bertscore_recall": [],

        "bertscore_f1": [],
    },
}

for sample in results:

    for model in ["base", "qlora"]:

        result = sample[model]
        reference = sample["reference"]
        prediction = sample[model]["response"]
        bleu_score = compute_bleu(
            reference,
            prediction,
        )
        rouge_scores = compute_rouge(
            reference,
            prediction,
        )       
        bert = compute_bertscore(
            reference,
            prediction,
        )
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
        metrics[model]["bleu"].append(
            bleu_score
        )

        metrics[model]["rouge1"].append(
            rouge_scores["rouge1"]
        )

        metrics[model]["rouge2"].append(
            rouge_scores["rouge2"]
        )

        metrics[model]["rougeL"].append(
            rouge_scores["rougeL"]
        )
        metrics[model]["bertscore_precision"].append(
            bert["precision"]
        )

        metrics[model]["bertscore_recall"].append(
            bert["recall"]
        )

        metrics[model]["bertscore_f1"].append(
            bert["f1"]
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
        "average_bleu": round(
            mean(metrics[model]["bleu"]),
            4,
        ),
        "average_rouge1": round(
            mean(metrics[model]["rouge1"]),
            4,
        ),
        "average_rouge2": round(
            mean(metrics[model]["rouge2"]),
            4,
        ),
        "average_rougeL": round(
            mean(metrics[model]["rougeL"]),
            4,
        ),
    }
    summary[model]["average_bertscore_precision"] = round(
        mean(metrics[model]["bertscore_precision"]),
        4,
        )

    summary[model]["average_bertscore_recall"] = round(
        mean(metrics[model]["bertscore_recall"]),
        4,
        )

    summary[model]["average_bertscore_f1"] = round(
        mean(metrics[model]["bertscore_f1"]),
        4,
        )


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