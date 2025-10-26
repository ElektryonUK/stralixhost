import asyncio
import time
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Deque, Tuple

from fastapi import Request, HTTPException

@dataclass
class RateLimitConfig:
    limit_per_minute: int


class InMemoryRateLimiter:
    def __init__(self):
        # key: (ip, route) -> deque[timestamps]
        self._buckets: dict[Tuple[str, str], Deque[float]] = defaultdict(deque)
        self._lock = asyncio.Lock()

    async def check(self, request: Request, limit: int) -> None:
        now = time.time()
        ip = request.client.host if request.client else "unknown"
        route = request.url.path
        key = (ip, route)
        cutoff = now - 60
        async with self._lock:
            bucket = self._buckets[key]
            # drop old entries
            while bucket and bucket[0] < cutoff:
                bucket.popleft()
            if len(bucket) >= limit:
                # compose headers
                remaining = max(0, limit - len(bucket))
                reset = int(cutoff + 60)
                raise HTTPException(status_code=429, detail="Too Many Requests")
            bucket.append(now)

rate_limiter = InMemoryRateLimiter()
