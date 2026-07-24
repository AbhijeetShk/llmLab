import json
import os
from dotenv import load_dotenv

load_dotenv()

from groq import Groq

MODEL = "llama-3.3-70b-versatile"

client = Groq(
    api_key=os.environ["GROQ_API_KEY"],
)


SYSTEM_PROMPT = """
You are an expert evaluator for Large Language Models.

Your task is to evaluate a candidate answer against the reference answer.

Evaluate ONLY the quality of the candidate answer.

Do not reward answers for matching wording.

Focus on semantic correctness.

Use the following rubric.

------------------------------------------------

Correctness (1-10)

How factually accurate is the answer?

10:
Completely correct.

7:
Mostly correct with minor issues.

4:
Contains important factual mistakes.

1:
Mostly incorrect.

------------------------------------------------

Completeness (1-10)

How completely does the answer address the instruction?

10:
Covers all major concepts.

7:
Misses small details.

4:
Misses several important ideas.

1:
Incomplete.

------------------------------------------------

Faithfulness (1-10)

Does the answer avoid unsupported or hallucinated information?

10:
Every statement is supported.

7:
Minor unsupported claims.

4:
Several hallucinations.

1:
Mostly fabricated.

------------------------------------------------

Helpfulness (1-10)

Would this answer genuinely help a user?

Consider:

- clarity
- organization
- conciseness
- readability

------------------------------------------------

Overall (1-10)

Overall quality considering all previous dimensions.

------------------------------------------------

Evaluation Rules

- Do NOT compare wording.

- Two answers with identical meaning should receive similar scores.

- Reward semantic correctness.

- Penalize hallucinations.

- Penalize missing concepts.

- Keep explanations concise.

Return ONLY valid JSON.

Example:

{
    "correctness": 9,
    "completeness": 8,
    "faithfulness": 10,
    "helpfulness": 9,
    "overall": 9,
    "reason": "Accurate answer with minor missing details."
}
"""


def judge_response(
    instruction,
    reference,
    prediction,
):

    prompt = f"""
Instruction:
{instruction}

Reference Answer:
{reference}

Candidate Answer:
{prediction}
"""

    completion = client.chat.completions.create(
        model=MODEL,
        temperature=0,
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