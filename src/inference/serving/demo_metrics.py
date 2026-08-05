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

print("Inference Metrics")
print()

print(f"Request ID                : {metrics.request_id}")

print(f"Input Tokens              : {metrics.input_tokens}")

print(f"Output Tokens             : {metrics.output_tokens}")

print(f"Total Tokens              : {metrics.total_tokens}")

print()

print(f"TTFT                      : {metrics.ttft_ms:.2f} ms")

print(f"Prefill Time              : {metrics.prefill_ms:.2f} ms")

print(f"Decode Time               : {metrics.decode_ms:.2f} ms")

print(f"End-to-End Latency        : {metrics.latency_ms:.2f} ms")

print()

print(f"Decode Tokens / Second    : {metrics.decode_tokens_per_second:.2f}")

print(f"Overall Tokens / Second   : {metrics.overall_tokens_per_second:.2f}")