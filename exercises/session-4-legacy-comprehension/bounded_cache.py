"""
bounded_cache.py — TTL + size-bounded memoization decorator.

Provides a decorator that caches function return values for a
configurable duration and evicts the least-recently-used entry when
the cache reaches its size limit.

Usage:
    from bounded_cache import cache

    @cache(maxsize=128, ttl=60)
    def fetch_rate(state_code: str) -> float:
        ...  # expensive call

    # Inspect or clear at runtime:
    fetch_rate.cache_info()
    fetch_rate.cache_clear()
"""

import functools
import hashlib
import pickle
import threading
import time
from collections import OrderedDict
from typing import Any, Callable, NamedTuple, Optional


class _CacheStats(NamedTuple):
    hits: int
    misses: int
    maxsize: int
    currsize: int
    ttl: float


class _Entry(NamedTuple):
    value: Any
    expires_at: float


_SENTINEL = object()


def cache(maxsize: int = 128, ttl: float = 300.0):
    """
    Decorator factory.  Returns a decorator that memoizes the wrapped
    function with an LRU eviction policy and per-entry TTL expiry.

    Parameters
    ----------
    maxsize : int
        Maximum number of entries to keep.  When full, the
        least-recently-used entry is evicted before inserting.
    ttl : float
        Seconds before a cached entry is considered stale.
        Stale entries are removed on the next access to that key.

    The decorated function gains three attributes:
        .cache_info()   -> _CacheStats
        .cache_clear()  -> None
        .cache_peek(key) -> value or None
    """
    if maxsize < 1:
        raise ValueError(f"maxsize must be >= 1, got {maxsize!r}")
    if ttl <= 0:
        raise ValueError(f"ttl must be > 0, got {ttl!r}")

    def decorator(fn: Callable) -> Callable:
        _store: OrderedDict[str, _Entry] = OrderedDict()
        _hits = 0
        _misses = 0
        _lock = threading.Lock()

        def _make_key(args: tuple, kwargs: dict) -> str:
            try:
                raw = pickle.dumps((args, sorted(kwargs.items())))
            except Exception:
                raw = repr((args, sorted(kwargs.items()))).encode()
            return hashlib.md5(raw).hexdigest()

        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            nonlocal _hits, _misses
            key = _make_key(args, kwargs)

            with _lock:
                entry = _store.get(key, _SENTINEL)
                if entry is not _SENTINEL:
                    if time.monotonic() < entry.expires_at:
                        _store.move_to_end(key)
                        _hits += 1
                        return entry.value
                    else:
                        del _store[key]

            result = fn(*args, **kwargs)

            with _lock:
                if key in _store:
                    _store.move_to_end(key)
                else:
                    if len(_store) >= maxsize:
                        _store.popitem(last=False)
                    _store[key] = _Entry(
                        value=result,
                        expires_at=time.monotonic() + ttl,
                    )
                _misses += 1

            return result

        def cache_info() -> _CacheStats:
            with _lock:
                return _CacheStats(
                    hits=_hits,
                    misses=_misses,
                    maxsize=maxsize,
                    currsize=len(_store),
                    ttl=ttl,
                )

        def cache_clear() -> None:
            nonlocal _hits, _misses
            with _lock:
                _store.clear()
                _hits = 0
                _misses = 0

        def cache_peek(key: str) -> Optional[Any]:
            with _lock:
                entry = _store.get(key, _SENTINEL)
                if entry is _SENTINEL:
                    return None
                if time.monotonic() >= entry.expires_at:
                    return None
                return entry.value

        wrapper.cache_info = cache_info
        wrapper.cache_clear = cache_clear
        wrapper.cache_peek = cache_peek
        return wrapper

    return decorator


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import random

    call_count = 0

    @cache(maxsize=3, ttl=2.0)
    def slow_lookup(state: str, year: int = 2024) -> float:
        global call_count
        call_count += 1
        time.sleep(0.05)
        return round(random.uniform(0.10, 0.25), 4)

    print("First pass — populating the cache:")
    for state in ("TX", "OK", "IL"):
        rate = slow_lookup(state)
        print(f"  {state}: {rate}  (calls so far: {call_count})")

    print("\nSecond pass — should be cache hits:")
    for state in ("TX", "OK", "IL"):
        rate = slow_lookup(state)
        print(f"  {state}: {rate}  (calls so far: {call_count})")

    print(f"\nCache info: {slow_lookup.cache_info()}")

    print("\nAdding a fourth entry — LRU (TX) should be evicted:")
    slow_lookup("KS")
    print(f"  Cache size: {slow_lookup.cache_info().currsize}")

    print("\nTX after eviction (should be a miss / new call):")
    slow_lookup("TX")
    print(f"  Total calls: {call_count}  (expected 5)")

    print("\nWaiting for TTL to expire (2.5 s)...")
    time.sleep(2.5)

    print("Post-TTL pass — should all be misses:")
    for state in ("OK", "IL", "TX"):
        slow_lookup(state)
    print(f"  Total calls: {call_count}  (expected 8)")
    print(f"  Cache info: {slow_lookup.cache_info()}")
