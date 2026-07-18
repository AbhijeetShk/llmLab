import time
from collections import deque
from dataclasses import dataclass


@dataclass
class Request:
    id: int
    output_tokens: int


waiting_queue = deque(
    [
        Request(1, 10),
        Request(2, 6),
        Request(3, 15),
        Request(4, 5),
        Request(5, 8),
        Request(6, 7),
        Request(7, 12),
    ]
)

BATCH_SIZE = 4

active = []


while len(active) < BATCH_SIZE and waiting_queue:
    active.append(waiting_queue.popleft())

step = 0

while active:

    step += 1

    print(f"\nGeneration Step {step}")

    finished = []

    for request in active:

        print(
            f"Request {request.id} -> Token"
        )

        request.output_tokens -= 1

        if request.output_tokens == 0:
            finished.append(request)


    for request in finished:

        print(
            f"Request {request.id} Finished"
        )

        active.remove(request)


    while len(active) < BATCH_SIZE and waiting_queue:

        new_request = waiting_queue.popleft()

        print(
            f"Adding Request {new_request.id}"
        )

        active.append(new_request)

    print(
        "Active:",
        [r.id for r in active]
    )

    time.sleep(0.5)

print("\nAll Requests Finished")