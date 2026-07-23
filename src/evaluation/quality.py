import evaluate
from bert_score import score as bertscore


bleu = evaluate.load("bleu")

rouge = evaluate.load("rouge")

def compute_bleu(reference, prediction):
    return bleu.compute(
        references=[reference],
        predictions=[prediction],
    )["bleu"]

def compute_rouge(reference, prediction):
    scores = rouge.compute(
        predictions=[prediction],
        references=[reference],
    )

    return scores
def compute_bertscore(
    reference,
    prediction,
):
    precision, recall, f1 = bertscore(
        [prediction],
        [reference],
        lang="en",
        verbose=False,
    )

    return {
        "precision": precision.item(),
        "recall": recall.item(),
        "f1": f1.item(),
    }