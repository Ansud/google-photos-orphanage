"""
Copyright: Copyright 2020 Anton Zelenov

This file is subject to the terms and conditions defined in
file 'LICENSE', which is part of this source code package.
"""

import os
import yaml
from typing import Dict
from flask import Flask
from common.redis import RedisClient


def load_config() -> Dict:
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '/../settings.yml')

    # TODO: Add error handling
    with open(path, 'r') as f:
        return yaml.load(f.read(), Loader=yaml.BaseLoader)


def create_application() -> Flask:
    config = load_config()

    application = Flask('google-photos-orphanage')
    application.config.from_mapping(config)

    # Initialize redis connection pool
    RedisClient(config['REDIS_CONNECTION'])

    return application
