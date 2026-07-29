from .engine import InferenceEngine
from .request import Request
from .generation_state import GenerationState

MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

engine = InferenceEngine(MODEL_NAME)

states = []

for i in range(3):

    state = GenerationState(

        Request(
            request_id=i,
            prompt=f"Explain concept {i}",
            max_new_tokens=10,
        )
    )

    states.append(state)

for state in states:

    result = engine.generate(state)

    print()

    print(f"Request {state.request.request_id}")

    print(result.generated_text)