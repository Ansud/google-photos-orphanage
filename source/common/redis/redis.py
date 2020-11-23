"""
Copyright: Copyright 2020 Anton Zelenov

This file is subject to the terms and conditions defined in
file 'LICENSE', which is part of this source code package.
"""

from redis import BlockingConnectionPool, Redis
from common.singleton import Singleton


class RedisClient(metaclass=Singleton):
    pool = None

    def __init__(self, custom_settings=None):
        if self.pool is None and custom_settings is None:
            raise Exception('Trying to use uninitialized RedisConnection class')

        settings = dict(
            decode_responses=True,
            retry_on_timeout=True,
        )

        settings.update(custom_settings)

        self.pool = BlockingConnectionPool(**settings)

    @property
    def instance(self):
        return Redis(connection_pool=self.pool)
