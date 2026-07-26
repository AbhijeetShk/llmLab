import json
import os

from dotenv import load_dotenv
from groq import Groq
from tqdm import tqdm

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = """
You are an expert evaluator of Large Language Model responses.

Your task is to identify the SINGLE most important quality issue in a candidate response.

Step 1:
Determine whether the response is acceptable.

A response is "Correct" if it:
- is factually accurate,
- adequately answers the instruction,
- contains no significant hallucinations,
- follows the instruction,
- would reasonably satisfy a user.

If ALL of the above are true, return "Correct".

Otherwise, choose exactly ONE primary failure category.

Failure Categories:

1. Hallucination
   - Contains unsupported or fabricated information.

2. Incorrect Facts
   - Contains factual errors or incorrect claims.

3. Incomplete
   - Omits important information needed to answer the instruction.

4. Poor Reasoning
   - The reasoning is flawed, contradictory, or logically incorrect.

5. Instruction Not Followed
   - Fails to follow the user's request or required format.

6. Poor Clarity
   - Difficult to understand due to poor organization, wording, or structure.

7. Unsafe
   - Contains harmful, dangerous, or inappropriate content.

8. Other
   - A meaningful defect that does not fit the above categories.

Rules:
- Choose EXACTLY ONE category.
- Prefer "Correct" whenever the response is acceptable.
- Do NOT invent issues simply because the response differs from the reference wording.
- Evaluate semantic quality, not writing style.
- Keep the explanation under 25 words.

Return ONLY valid JSON in this format:

{
    "category": "Correct",
    "confidence": 10,
    "reason": "Accurate and sufficiently complete."
}
"""
def analyze(
    instruction,
    reference,
    prediction,
    evaluation,
):

    prompt = f"""
Instruction:
{instruction}

Reference Answer:
{reference}

Candidate Response:
{prediction}

Previous Evaluation:
- Correctness: {evaluation["correctness"]}/10
- Completeness: {evaluation["completeness"]}/10
- Faithfulness: {evaluation["faithfulness"]}/10
- Helpfulness: {evaluation["helpfulness"]}/10
- Overall: {evaluation["overall"]}/10
- Judge Reason: {evaluation["reason"]}

Based on the response AND the previous evaluation,
identify the SINGLE primary failure category.

If the response is acceptable overall,
return "Correct".
"""

    completion = client.chat.completions.create(
        model=MODEL,
        temperature=0, #in evaluation it makes the judge more deterministic
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    return json.loads(
        completion.choices[0].message.content
    )


def print_contradiction_examples(results, limit=5):
    contradictions = []

    for sample in results:
        for model in ["base", "qlora"]:
            model_result = sample.get(model, {})
            evaluation = model_result.get("evaluation", {})
            failure = model_result.get("failure_diagnosis", {})

            if evaluation.get("overall", 0) >= 9 and failure.get("category") == "Incomplete":
                contradictions.append(
                    {
                        "model": model,
                        "overall": evaluation.get("overall"),
                        "category": failure.get("category"),
                        "reason": failure.get("reason"),
                        "instruction": sample.get("instruction", ""),
                        "response": model_result.get("response", ""),
                    }
                )

    print(
        f"Found {len(contradictions)} contradiction cases "
        f"(overall >= 9 and failure category = Incomplete)."
    )

    for item in contradictions[:limit]:
        print("-" * 80)
        print(f"Model: {item['model']}")
        print(f"Overall: {item['overall']}/10")
        print(f"Failure category: {item['category']}")
        print(f"Reason: {item['reason']}")
        print(f"Instruction: {item['instruction'][:220]}")
        print(f"Response: {item['response'][:400]}")


INPUT = "outputs/judge_results.json"
OUTPUT = "outputs/failure_analysis.json"

with open(INPUT, "r", encoding="utf-8") as f:
    results = json.load(f)

analysis_results = []

for sample in tqdm(results):

    row = {
        "instruction": sample["instruction"],
        "reference": sample["reference"],
    }

    for model in ["base", "qlora"]:

        response = sample[model]["response"]
        evaluation = sample[model]["evaluation"]

        failure = analyze(
            sample["instruction"],
            sample["reference"],
            response,
            evaluation,
        )

        row[model] = {
            "response": response,
            "evaluation": evaluation,
            "failure_diagnosis": failure, # isnt just analysis but contains the model's diagnosis (category, confidence, and reason)
        }

    analysis_results.append(row)

print_contradiction_examples(analysis_results)

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(
        analysis_results,
        f,
        indent=2,
        ensure_ascii=False,
    )

print("Failure analysis complete.")