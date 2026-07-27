from .kv_cache import KVCache


cache = KVCache()

dummy_cache_1 = ("layer1", "layer2")
dummy_cache_2 = ("layerA", "layerB")

cache.set(1, dummy_cache_1)
cache.set(2, dummy_cache_2)

print(cache.contains(1))
print(cache.contains(2))

print(cache.num_requests())

print(cache.active_request_ids())

print(cache.get(1))

cache.remove(1)

print(cache.contains(1))

print(cache.num_requests())

cache.clear()

print(cache.num_requests())