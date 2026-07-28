from collections import deque

from .request import Request


class Scheduler:
  
    #round-robin scheduler for active generation requests.


    def __init__(self):
        self.queue = deque()

    def submit(self, request: Request):
        self.queue.append(request)

    def next(self) -> Request | None:
       #return next request to decode
        if not self.queue:
            return None

        return self.queue.popleft()

    def reschedule(self, request: Request):
        #reschedule an unfinished req to the end
        if not request.is_finished():
            self.queue.append(request)

    def has_requests(self):
        return len(self.queue) > 0

    def size(self):
        return len(self.queue)