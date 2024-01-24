#!/usr/bin/env python3
"""Create a Cache class."""
import redis
import uuid
from typing import Callable, Optional, Union
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of calls to a method and
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrap function"""
        key = method.__qualname__
        count = self._redis.incr(key)
        result = method(self, *args, **kwargs)
        return result
    return wrapper


def call_history(method: Callable) -> Callable:
    """call_history decorator"""
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper for the deco"""
        self._redis.rpush(inputs, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(result))
        return result
    return wrapper


def replay(method: Callable) -> None:
    """replay function"""
    method_name = method.__qualname__
    cache = redis.Redis()
    calls = cache.get(method_name).decode("utf-8")
    print("{} was called {} times:".format(method_name, calls))
    inputs = cache.lrange(method_name + ":inputs", 0, -1)
    outputs = cache.lrange(method_name + ":outputs", 0, -1)
    for i, o in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(method_name, i.decode('utf-8'),
                                     o.decode('utf-8')))


class Cache():
    """Cache class"""
    def __init__(self) -> None:
        """cache class to interact with redis"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """STORE METHOD"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, None]:
        """to convert the data back to the desired format."""
        if fn:
            return fn(self._redis.get(key))
        else:
            return self._redis.get(key)

    def get_str(self, key: str) -> str:
        """automatically parametrize Cache.get with the correct conversion"""
        return self.get(key, str)

    def get_int(self, key: int) -> int:
        """automatically parametrize Cache.get with the correct conversion"""
        return self.get(key, int)
