from ..engine.engine import InferenceEngine
from ..engine.generation_state import GenerationState


class GenerationSession:

    def __init__(
        self,
        engine: InferenceEngine,
        state: GenerationState,
    ):

        self.engine = engine
        self.state = state
        self._decoded_length = 0 #decode the accumulated sequence and emit only
        # the newly generated suffix

    def start(self):

        self.engine.prefill(
            self.state
        )

    def step(self):

        self.engine.step(
            self.state
        )

    def is_finished(self):

        return self.state.request.is_finished()

    def current_token(self):

        if self.state.last_token is None:
            return None

        return self.engine.worker.tokenizer.decode(
            [self.state.last_token.item()],
            skip_special_tokens=True,
        )

    def generated_text(self):

        return self.engine.worker.decode_tokens(
            self.state.request.generated_tokens
        )
    def next_text_chunk(self):

        text = self.generated_text()

        delta = text[self._decoded_length :]

        self._decoded_length = len(text)

        return delta