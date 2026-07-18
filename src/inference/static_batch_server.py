import time
from dataclasses import dataclass


@dataclass
class Request:
    id: int
    output_tokens: int


requests = [
    Request(1, 10),
    Request(2, 6),
    Request(3, 15),
    Request(4, 5),
]

batch_size = len(requests)

print(f"Running Batch Size = {batch_size}")

start = time.perf_counter()

max_tokens = max(r.output_tokens for r in requests)

for step in range(max_tokens):

    print(f"\nGeneration Step {step + 1}")

    for request in requests:

        if step < request.output_tokens:

            print(
                f"Request {request.id} -> Token {step + 1}"
            )

        else:

            print(
                f"Request {request.id} -> PAD"
            )

    time.sleep(0.05)

end = time.perf_counter()

print(f"\nTotal Time: {end-start:.2f} sec")