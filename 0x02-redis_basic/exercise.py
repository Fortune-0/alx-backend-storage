#!/usr/bin/env python3
""" Redis client module
"""
import redis
import uuid
from typing import Any, Callable, Optional, Union


class Cache:
    """ Caching class
    """
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Stores data in redis with randomly generated key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return (key)
