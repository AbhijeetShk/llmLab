from .worker import ModelWorker
from .sampler import Sampler
from .kv_cache import KVCache
from .scheduler import Scheduler
from .request import Request


class InferenceEngine:

    def __init__(self, model_name: str):

        self.worker = ModelWorker(model_name)

        self.scheduler = Scheduler()

        self.cache = KVCache()

        self.sampler = Sampler()

#initialize req

    def prefill(self, request: Request):
#performs the initial forward pass for a request, initializes the KV cache, and returns the first token.
        input_ids = self.worker.encode(
            request.prompt
        )

        logits, past_key_values = self.worker.prefill(
            input_ids
        )

        self.cache.set(
            request.request_id,
            past_key_values,
        )

        next_token = self.sampler.greedy(
            logits
        )

        request.append_token(
            next_token.item()
        )

        return next_token

#one token decode only

    def step(
        self,
        request: Request,
        last_token,
    ):

        cache = self.cache.get(
            request.request_id
        )

        logits, cache = self.worker.decode(
            last_token,
            cache,
        )

        self.cache.set(
            request.request_id,
            cache,
        )

        next_token = self.sampler.greedy(
            logits
        )

        request.append_token(
            next_token.item()
        )

        return next_token

#full generation loop

def generate(
    self,
    request: Request,
):

    next_token = self.prefill(request)

    try:
        while not request.is_finished():
            next_token = self.step(
                request,
                next_token,
            )

        request.update_text(
            self.worker.decode_tokens(
                request.generated_tokens
            )
        )

        request.mark_finished()

        return request

    finally:
        self.cache.remove(
            request.request_id
        )