import torch

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
)

MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)
device = "cuda" if torch.cuda.is_available() else "cpu"
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME
)

model.eval()


def ask(question: str):

    prompt = f"""->Instruction:
{question}

-> Response:
"""

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
    ).to(device)

    with torch.no_grad():

        outputs = model.generate(
            **inputs,
            max_new_tokens=32,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
        )

    answer = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True,
    )

    print("\n" + "=" * 80)
    print(question)
    print("=" * 80)
    print(answer)
    print()


questions = [
    "What is RAG?",
    "What is Hybrid Search?",
    "What is LangGraph?",
    "Explain LoRA.",
]

for q in questions:
    print(f"\nGenerating answer for: {q}")
    ask(q)
    print("Generation complete")