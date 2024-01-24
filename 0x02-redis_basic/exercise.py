#!/usr/bin/env python3
"""Create a Cache class."""
import redis
import uuid
from typing import Callable, Optional, Union


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

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, None]:
        """to convert the data back to the desired format."""
        if fn:
            return fn(self._redis.get(key))
        else:
            return self._redis.get(key)
    
    def get_str(self, key:str) -> str:
        """automatically parametrize Cache.get with the correct conversion function"""
        return self.get(key, str)
    
    def get_int(self, key:int) -> int:
        """automatically parametrize Cache.get with the correct conversion function"""
        return self.get(key, int)
