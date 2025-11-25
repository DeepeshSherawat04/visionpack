# src/utils/cache.py

from __future__ import annotations
import hashlib
from typing import Any, Dict, Optional


class PredictionCache:
    def __init__(self, max_items: int = 128) -> None:
        self.max_items = max_items
        self._store: Dict[str, Any] = {}

    @staticmethod
    def make_key(data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()

    def get(self, key: str) -> Optional[Any]:
        return self._store.get(key)

    def set(self, key: str, value: Any) -> None:
        if len(self._store) >= self.max_items:
            # naive eviction: pop first item
            first_key = next(iter(self._store))
            self._store.pop(first_key, None)
        self._store[key] = value


prediction_cache = PredictionCache()
