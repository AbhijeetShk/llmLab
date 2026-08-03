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

        if not self._queue:
            return None

        return self._queue.popleft()

    def empty(self):

        return len(self._queue) == 0

    def size(self):

        return len(self._queue)