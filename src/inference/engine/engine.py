from .worker import ModelWorker
from .sampler import Sampler
from .kv_cache import KVCache
from .scheduler import Scheduler
from .generation_state import GenerationState


class InferenceEngine:

    def __init__(self, model_name: str):

        self.worker = ModelWorker(model_name)

        self.scheduler = Scheduler()

        self.cache = KVCache()

        self.sampler = Sampler()

#initialize req

    def prefill(self, state: GenerationState):
#performs the initial forward pass for a request, initializes the KV cache, and returns the first token.

        input_ids = self.worker.encode(
            state.request.prompt
        )

        logits, past_key_values = self.worker.prefill(
            input_ids
        )

        self.cache.set(
            state.request.request_id,
            past_key_values,
        )

        state.last_token = self.sampler.greedy(
            logits
        )

        state.request.append_token(
            state.last_token.item()
        )

#one token decode only

    def step(
        self,
        state: GenerationState,
    ):

        cache = self.cache.get(
            state.request.request_id
        )

        logits, cache = self.worker.decode(
            state.last_token,
            cache,
        )

        self.cache.set(
            state.request.request_id,
            cache,
        )

        state.last_token = self.sampler.greedy(
            logits
        )

        state.request.append_token(
            state.last_token.item()
        )

#full generation loop

    def generate(
        self,
        state: GenerationState,
    ):

        self.prefill(state)

        try:

            while not state.request.is_finished():

                self.step(state)

            state.request.update_text(
                self.worker.decode_tokens(
                    state.request.generated_tokens
                )
            )

            state.request.mark_finished()

            return state.request

        finally:

            self.cache.remove(
                state.request.request_id
            )