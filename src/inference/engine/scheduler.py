from collections import deque


class Scheduler:

   #Maintains waiting requests.


    def __init__(self):

        self.queue = deque()

    def submit(self, request):

        self.queue.append(request)

    def next_batch(self, batch_size):

        batch = []

        while self.queue and len(batch) < batch_size:
            batch.append(self.queue.popleft())

        return batch

    def empty(self):

        return len(self.queue) == 0