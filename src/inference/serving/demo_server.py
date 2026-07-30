from ..engine.request import Request

from .server import InferenceServer


MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

server = InferenceServer(
    MODEL
)

request = Request(
    request_id=1,
    prompt="Explain KV Cache.",
    max_new_tokens=20,
)

response = server.generate(
    request
)

print()

print(response.generated_text)