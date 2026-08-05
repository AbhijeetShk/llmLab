from dataclasses import dataclass


@dataclass
class InferenceMetrics:

    request_id: int

    ttft_ms: float

    latency_ms: float

    output_tokens: int

    tokens_per_second: float