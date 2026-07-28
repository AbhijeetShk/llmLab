from .request import Request
from .generation_state import GenerationState


request = Request(
    request_id=1,
    prompt="Explain LoRA."
)

state = GenerationState(request)

print(state)
print()

print("Request:")
print(state.request)

print()

print("Last token:")
print(state.last_token)