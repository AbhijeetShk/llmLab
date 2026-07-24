import json
import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = """
You are an expert evaluator for Large Language Models.

You will compare two candidate responses.

Evaluate ONLY semantic quality.

Ignore writing style unless it affects clarity.

Judge according to:

- correctness
- completeness
- faithfulness
- helpfulness

Choose ONLY ONE:

"A"

"B"

"Tie"

Be strict.

Return ONLY JSON.

{
    "winner":"A",
    "confidence":9,
    "reason":"A is more complete while remaining accurate."
}
"""


def compare(
    instruction,
    reference,
    answer_a,
    answer_b,
):

    prompt = f"""
Instruction:

{instruction}

Reference:

{reference}

Response A:

{answer_a}

Response B:

{answer_b}
"""

    response = client.chat.completions.create(
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
        response.choices[0].message.content
    )