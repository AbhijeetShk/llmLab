from ..engine.engine import InferenceEngine
from ..engine.request import Request
from ..engine.generation_state import GenerationState

from .queue import RequestQueue
from .session import GenerationSession
from .stream import StreamIterator


class InferenceServer:

    def __init__(
        self,
        model_name: str,
    ):

        self.engine = InferenceEngine(
            model_name
        )

        self.queue = RequestQueue()

    def create_session(
        self,
        request: Request,
    ):

        state = GenerationState(
            request
        )

        return GenerationSession(
            self.engine,
            state,
        )

    def _acquire_session(
        self,
        request: Request,
    ):

        session = self.create_session(
            request
        )

        self.queue.push(
            session
        )

        return self.queue.pop()


    def generate(
        self,
        request: Request,
    ):

        session = self._acquire_session(
            request
        )

        session.start()

        while not session.is_finished():

            session.step()

        request.update_text(
            session.generated_text()
        )

        request.mark_finished()

        return request
    

    def generate_batch(
        self,
        requests: list[Request],
        ):

        for request in requests:

            session = self.create_session(
                request
            )

            self.queue.push(session)

        batch = self.queue.pop_batch(
            batch_size=len(requests),)
        
        states = [
            session.state
        for session in batch]

        responses = self.engine.generate_batch(
            states
        )
        return responses
        

    def stream(
        self,
        request: Request,
    ):

        session = self._acquire_session(
            request
        )

        return StreamIterator(
            session
        )