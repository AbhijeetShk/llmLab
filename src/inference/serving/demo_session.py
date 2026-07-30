from ..engine.engine import InferenceEngine
from ..engine.request import Request
from ..engine.generation_state import GenerationState

from .session import GenerationSession

MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

engine = InferenceEngine(MODEL)

session = GenerationSession(
    engine,
    GenerationState(
        Request(
            request_id=1,
            prompt="Explain KV Cache.",
            max_new_tokens=20,
        )
    ),
)

session.start()

while not session.is_finished():

    session.step()

    print(
        session.current_token(),
        end="",
        flush=True,
    )

print()

print(session.generated_text())