#!/usr/bin/env python3
"""Create a Cache class."""
import redis
import uuid
from typing import Union


class Cache():
    """Cache class"""
    def __init__(self) -> None:
        """cache class to interact with redis"""
        self._redis = redis.Redis();
        self._redis.flushdb()
    
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """STORE METHOD"""
        key=str(uuid.uuid4())
        self._redis.set(key, data)
        return key
