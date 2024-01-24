#!/usr/bin/env python3
""" requests module to obtain the HTML content of a particular URL """

from functools import wraps
import redis
import requests


# Connect to Redis
redis_client = redis.Redis()


def cache_result(expires=10):
    """
    Decorator for caching the result of a function with an expiration time.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(url):
            count_key = f"count:{url}"
            result_key = f"result:{url}"

            # Check if the URL is in the cache
            if not redis_client.get(count_key):
                redis_client.set(count_key, 1)
                result = func(url)
                redis_client.setex(result_key, expires, result)
            else:
                redis_client.incr(count_key)
                result = redis_client.get(result_key)

            return result
        return wrapper
    return decorator


@cache_result()
def get_page(url: str) -> str:
    """Implement a get_page function."""
    return requests.get(url).text
