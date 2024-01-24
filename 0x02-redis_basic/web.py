#!/usr/bin/env python3
""" requests module to obtain the HTML content of a particular URL """

from functools import wraps
import redis
import requests
from typing import Callable

redis_ = redis.Redis()


def count_requests(method: Callable) -> Callable:
    """ Decortator counter"""
    @wraps(method)
    def wrapper(url):  # sourcery skip: use-named-expression
        """Wrapper for decorator"""
        redis_.incr("count:{}".format(url))
        cached_html = redis_.get("cached:{}".format(url))
        if cached_html:
            return cached_html.decode('utf-8')
        html = method(url)
        redis_.setex("cached:{}".format(url), 10, html)
        return html

    return wrapper


@count_requests
def get_page(url: str) -> str:
    """ Obtain the HTML content of a  URL """
    req = requests.get(url)
    return req.text
