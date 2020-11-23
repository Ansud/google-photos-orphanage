"""
Copyright: Copyright 2020 Anton Zelenov

This file is subject to the terms and conditions defined in
file 'LICENSE', which is part of this source code package.
"""

from common.redis import RedisClient
import json


class RedisQueue:
    def __init__(self, name):
        self.name = f'GPO:Q:{name}'
        self.redis = RedisClient().instance

    def push(self, data):
        self.redis.rpush(self.name, json.dumps(data))

    def poll(self):
        return json.loads(self.redis.blpop(self.name))
