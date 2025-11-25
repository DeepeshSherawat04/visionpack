from src.utils.cache import PredictionCache, prediction_cache


def test_prediction_cache_basic():
    cache = PredictionCache(max_items=2)

    key1, key2, key3 = "k1", "k2", "k3"
    cache.set(key1, {"v": 1})
    cache.set(key2, {"v": 2})

    assert cache.get(key1)["v"] == 1
    assert cache.get(key2)["v"] == 2

    # adding a third item should evict one of the previous keys
    cache.set(key3, {"v": 3})
    assert cache.get(key3)["v"] == 3
    assert len(cache._store) <= 2


def test_prediction_cache_global_instance():
    # ensure global cache can store and retrieve
    key = prediction_cache.make_key(b"hello")
    prediction_cache.set(key, {"ok": True})
    assert prediction_cache.get(key)["ok"] is True
