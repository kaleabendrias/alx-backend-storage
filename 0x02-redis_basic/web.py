#!/usr/bin/env python3
""" requests module to obtain the HTML content of a particular URL """

from functools import wraps
import redis
import requests
from typing import Callable

redis_ = redis.Redis()


def get_page(url: str) -> str:
    """we will implement a get_page function ."""
    result = requests.get(url).text
    if not redis_.get("count:{}".format(url)):
        redis_.set("count:{}".format(url), 1)
        redis_.setex("result:{}".format(url), 10, result)
    else:
        redis_.incr("count:{}".format(url), 1)
    return result
