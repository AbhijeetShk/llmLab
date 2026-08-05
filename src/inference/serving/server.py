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

    def _execute(
        self,
        request: Request,
        collect_metrics: bool = False,
    ):

        start = time.perf_counter()

        session = self._acquire_session(
            request
        )

        input_ids = self.engine.worker.encode(
            request.prompt
        )

        input_tokens = input_ids.shape[-1]

        session.start()

        prefill_end = time.perf_counter()

        while not session.is_finished():

            session.step()

        end = time.perf_counter()

        request.update_text(
            session.generated_text()
        )

        request.mark_finished()

        if not collect_metrics:

            return request

        output_tokens = request.generated_length()

        total_tokens = (
            input_tokens
            + output_tokens
        )

        prefill_ms = (
            prefill_end - start
        ) * 1000

        decode_ms = (
            end - prefill_end
        ) * 1000

        latency_ms = (
            end - start
        ) * 1000

        ttft_ms = prefill_ms

        decode_tokens_per_second = (
            output_tokens
            /
            max(
                decode_ms / 1000,
                1e-6,
            )
        )

        overall_tokens_per_second = (
            output_tokens
            /
            max(
                latency_ms / 1000,
                1e-6,
            )
        )

        metrics = InferenceMetrics(

            request_id=request.request_id,

            input_tokens=input_tokens,

            output_tokens=output_tokens,

            total_tokens=total_tokens,

            ttft_ms=ttft_ms,

            prefill_ms=prefill_ms,

            decode_ms=decode_ms,

            latency_ms=latency_ms,

            decode_tokens_per_second=decode_tokens_per_second,

            overall_tokens_per_second=overall_tokens_per_second,
        )

        return request, metrics
    def generate(
        self,
        request: Request,
    ):

        return self._execute(
            request,
            collect_metrics=False,
        )
    

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

        return self._execute(
            request,
            collect_metrics=True,
        )