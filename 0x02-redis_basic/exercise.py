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

    def get(self, key: str, fn: Optional[callable] =
            None) -> Union[str, bytes, int, float]:
        value = self._redis.get(key)
        if value is not None and fn is not None:
            return fn(value)

    def get_int(self, key: str) -> int:
        """
        Retrieves the integer value associated with the given key from Redis.

        Parameters:
        key (str): The key of the value to retrieve.

        Returns:
        int: The integer value associated with the given key.
        If the key does not exist or the value is not an integer, returns None.

        Note:
        This method uses the `get` method of the Cache class to retrieve
        the value and applies the `int` function to convert it to an integer.
        """
        return self.get(key, fn=int)

    def get_str(self, key: str) -> str:
        """
        Retrieves the value associated with the given key from
        Redis and decodes it as a string.

        Parameters:
        key (str): The key of the value to retrieve.

        Returns:
        str: The decoded value associated with the given key.
        If the key does not exist or the value is not a string, returns None.

        Note:
        This method uses the `get` method of the Cache class to retrieve
        the value and applies a lambda function to decode it as a string.
        """
        return self.get(key, fn=lambda x: x.decode('utf8()'))

    def count_calls(method: Callable) -> Callable:
        """ Decorator for Cache class methods to track call count
        """
        @functools.wraps(method)
        def wrapper(self: Any, *args, **kwargs) -> str:
            """ Wraps called method and adds its call count
            redis before execution
            """
            self._redis.incr(method.__qualname__)
            return method(self, *args, **kwargs)
        return wrapper

    @count_calls
    def store(self, data: Union[str, bytes,  int,  float]) -> str:

        """ Stores data in redis with randomly generated key
        """
        key = str(uuid4())
        client = self._redis
        client.set(key, data)
        return key

    def call_history(method: Callable) -> Callable:

        """ Decorator for Cache class method to track args
        """
    @wraps(method)
    def wrapper(self: Any, *args) -> str:
        """ Wraps called method and tracks its passed argument by storing
            them to redis
        """
        self._redis.rpush(f'{method.__qualname__}:inputs', str(args))
        output = method(self, *args)
        self._redis.rpush(f'{method.__qualname__}:outputs', output)
        return output
        return wrapper
