from collections import deque

from .session import GenerationSession


class RequestQueue:

    def __init__(self):

        self._queue = deque()

    def push(
        self,
        session: GenerationSession,
    ):

        self._queue.append(session)

    def pop(self):

        if self.empty():
            return None

        return self._queue.popleft()


    def pop_batch(
     self,
        batch_size,):

        batch = []

        while (
            not self.empty()
            and len(batch) < batch_size
        ):

            batch.append(
                self._queue.popleft()
            )

        return batch

    def empty(self):

        return len(self._queue) == 0

    def size(self):

        return len(self._queue)