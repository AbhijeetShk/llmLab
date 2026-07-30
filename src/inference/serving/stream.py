from typing import Iterator

from src.inference.engine.engine import InferenceEngine
from src.inference.engine.generation_state import GenerationState


class StreamIterator:

    def __init__(
        self,
        engine: InferenceEngine,
        state: GenerationState,
    ):

        self.engine = engine

        self.state = state

    def __iter__(self):

        return self

    def __next__(self):

        if self.state.request.is_finished():

            raise StopIteration

        if self.state.last_token is None:

            self.engine.prefill(
                self.state
            )

        else:

            self.engine.step(
                self.state
            )

        token = self.state.last_token.item()

        if (
            token
            == self.engine.worker.tokenizer.eos_token_id
        ):

            self.state.request.mark_finished()

        return self.engine.worker.tokenizer.decode(
            [token],
            skip_special_tokens=True,
        )