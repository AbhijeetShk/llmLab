from ..engine.engine import InferenceEngine
from ..engine.request import Request
from ..engine.generation_state import GenerationState

from .queue import RequestQueue
from .session import GenerationSession
from .stream import StreamIterator
import time

from .metrics import InferenceMetrics

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
    def measure(
    self,
    request: Request,
):

        start = time.perf_counter()

        session = self._acquire_session(
            request
        )

        session.start()

        ttft = (
            time.perf_counter()
            - start
        ) * 1000

        while not session.is_finished():

            session.step()

        latency = (
            time.perf_counter()
            - start
        ) * 1000

        request.update_text(
            session.generated_text()
        )

        request.mark_finished()

        output_tokens = request.generated_length()

        generation_time = max(
            latency - ttft,
            1e-6,
        )

        tokens_per_second = (
            output_tokens
            /
            (generation_time / 1000)
        )

        metrics = InferenceMetrics(

            request_id=request.request_id,

            ttft_ms=ttft,

            latency_ms=latency,

            output_tokens=output_tokens,

            tokens_per_second=tokens_per_second,
        )

        return request, metrics