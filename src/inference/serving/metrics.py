from dataclasses import dataclass


@dataclass
class InferenceMetrics:

    request_id: int

    input_tokens: int

    output_tokens: int

    total_tokens: int

    ttft_ms: float

    prefill_ms: float

    decode_ms: float

    latency_ms: float

    average_decode_time_ms: float
    
    decode_tokens_per_second: float

    overall_tokens_per_second: float