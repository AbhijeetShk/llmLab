from .engine import InferenceEngine
from .request import Request

MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

engine = InferenceEngine(MODEL_NAME)

engine.submit(
    Request(
        request_id=1,
        prompt="Explain LoRA."
    )
)

engine.submit(
    Request(
        request_id=2,
        prompt="Explain RAG."
    )
)

print(engine.pending())

batch = engine.scheduler.next_batch(2)

for request in batch:
    print(request)