class KVCache:
 
    #stores KV cache for each active request.


    def __init__(self):

        self.cache = {}

    def get(self, request_id):

        return self.cache.get(request_id)

    def update(self, request_id, kv):

        self.cache[request_id] = kv

    def remove(self, request_id):

        self.cache.pop(request_id, None)

    def clear(self):

        self.cache.clear()

    def __len__(self):

        return len(self.cache)