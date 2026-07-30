from ..engine.engine import InferenceEngine
from ..engine.request import Request
from ..engine.generation_state import GenerationState

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

    def generate(
        self,
        request: Request,
    ):

        session = self.create_session(
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

    def stream(
        self,
        request: Request,
    ):

        session = self.create_session(
            request
        )

        return StreamIterator(
            session
        )