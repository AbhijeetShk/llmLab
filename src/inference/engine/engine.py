from .kv_cache import KVCache
from .scheduler import Scheduler
from .worker import ModelWorker


class InferenceEngine:

    def __init__(self, model_name):

        self.scheduler = Scheduler()

        self.kv_cache = KVCache()

        self.worker = ModelWorker(model_name)

    def submit(self, request):

        self.scheduler.submit(request)

    def pending(self):

        return not self.scheduler.empty()