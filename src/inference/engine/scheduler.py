from collections import deque

from .generation_state import GenerationState


class Scheduler:
  
    #round-robin scheduler for active generation requests.


    def __init__(self):
        self.queue = deque()

    def submit(self, state: GenerationState):

        self.queue.append(state)

    def next(self):

#return next request to decode
        if not self.queue:
            return None

        return self.queue.popleft()
    
    def next_batch(
        self,
        batch_size: int,
    ):

        batch = []

        while self.queue and len(batch) < batch_size:

            batch.append(
                self.queue.popleft()
            )

        return batch
    
    def reschedule(self, state: GenerationState):
        #reschedule an unfinished req to the end
        if not state.request.is_finished():
            self.queue.append(state)

    def has_requests(self):
        return len(self.queue) > 0

    def size(self):
        return len(self.queue)