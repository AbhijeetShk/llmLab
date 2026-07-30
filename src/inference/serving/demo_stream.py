from src.inference.engine.engine import InferenceEngine
from src.inference.engine.request import Request
from src.inference.engine.generation_state import GenerationState

from src.inference.serving.stream import StreamIterator


MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

engine = InferenceEngine(MODEL)

state = GenerationState(

    Request(

        request_id=1,

        prompt="Explain Transformers in one sentence.",

        max_new_tokens=30,
    )
)

stream = StreamIterator(
    engine,
    state,
)

print()

for token in stream:

    print(
        token,
        end="",
        flush=True,
    )

print()