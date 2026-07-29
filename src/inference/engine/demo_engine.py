from .engine import InferenceEngine
from .generation_state import GenerationState
from .request import Request

MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

engine = InferenceEngine(MODEL_NAME)

states = []

for i in range(3):

    states.append(

        GenerationState(

            Request(

                request_id=i,
                prompt=f"Explain transformers {i}",
                max_new_tokens=10,
            )
        )
    )

results = engine.generate_batch(states)

for request in results:

    print("=" * 60)
    print(f"Request {request.request_id}")
    print(request.generated_text)