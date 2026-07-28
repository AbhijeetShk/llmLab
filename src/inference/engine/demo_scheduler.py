from .scheduler import Scheduler
from .request import Request

scheduler = Scheduler()

r1 = Request(
    request_id=1,
    prompt="Explain LoRA."
)

r2 = Request(
    request_id=2,
    prompt="Explain RAG."
)

scheduler.submit(r1)
scheduler.submit(r2)

print("Queue size:", scheduler.size())

request = scheduler.next()

print("Dequeued:", request.request_id)

scheduler.reschedule(request)

print("Queue size after reschedule:", scheduler.size())