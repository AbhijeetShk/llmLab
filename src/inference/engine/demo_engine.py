from .engine import InferenceEngine
from .request import Request
from .generation_state import GenerationState

MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

engine = InferenceEngine(MODEL_NAME)

request = Request(
    request_id=1,
    prompt="Explain LoRA."
)

state = GenerationState(request)

result = engine.generate(state)

print()

print("Generated text:")

print(result.generated_text)