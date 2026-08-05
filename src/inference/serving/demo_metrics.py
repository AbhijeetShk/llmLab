from ..engine.request import Request

from .server import InferenceServer


MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

server = InferenceServer(
    MODEL
)

request = Request(
    request_id=1,
    prompt="Explain Retrieval Augmented Generation.",
    max_new_tokens=64,
)

response, metrics = server.measure(
    request
)

print()

print(response.generated_text)

print()

print()

print(f"TTFT: {metrics.ttft_ms:.2f} ms")

print(f"Latency: {metrics.latency_ms:.2f} ms")

print(f"Output Tokens: {metrics.output_tokens}")

print(f"Tokens / Second: {metrics.tokens_per_second:.2f}")