from typing import Any


class KVCache:

    """
    Stores transformer KV caches for every active request.
    """

    def __init__(self):

        self._cache: dict[int, Any] = {}



    def set(
        self,
        request_id: int,
        past_key_values,
    ):

        self._cache[request_id] = past_key_values

    def get(
        self,
        request_id: int,
    ):

        return self._cache.get(request_id)

    def remove(
        self,
        request_id: int,
    ):

        self._cache.pop(request_id, None)

    def clear(self):

        self._cache.clear()



    def contains(
        self,
        request_id: int,
    ) -> bool:

        return request_id in self._cache

    def num_requests(self):

        return len(self._cache)

    def active_request_ids(self):

        return list(self._cache.keys())