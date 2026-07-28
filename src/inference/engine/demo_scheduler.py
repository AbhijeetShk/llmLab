from .scheduler import Scheduler
from .request import Request
from .generation_state import GenerationState

scheduler = Scheduler()

state1 = GenerationState(
    Request(
        request_id=1,
        prompt="Explain LoRA."
    )
)

state2 = GenerationState(
    Request(
        request_id=2,
        prompt="Explain RAG."
    )
)

scheduler.submit(state1)
scheduler.submit(state2)

print("Queue size:", scheduler.size())

state = scheduler.next()

print("Dequeued:", state.request.request_id)

scheduler.reschedule(state)

print("Queue size after reschedule:", scheduler.size())