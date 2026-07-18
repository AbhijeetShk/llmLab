import random
import time
from dataclasses import dataclass


@dataclass
class Request:
    id: int
    prompt_length: int
    output_tokens: int


def generate(request: Request):
    print(f"\nServing Request {request.id}")

    for token in range(request.output_tokens):
        print(
            f"Request {request.id} -> Token {token + 1}/{request.output_tokens}"
        )
        time.sleep(0.05)

    print(f"Finished Request {request.id}")


requests = [
    Request(1, 120, 10),
    Request(2, 80, 6),
    Request(3, 300, 15),
    Request(4, 40, 5),
]

start = time.perf_counter()

for request in requests:
    generate(request)

end = time.perf_counter()

print(f"\nTotal Time: {end - start:.2f} sec")