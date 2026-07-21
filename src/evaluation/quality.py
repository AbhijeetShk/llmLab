import evaluate

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