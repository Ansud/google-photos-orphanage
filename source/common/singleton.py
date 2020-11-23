"""
Copyright: Copyright 2020 Anton Zelenov

This file is subject to the terms and conditions defined in
file 'LICENSE', which is part of this source code package.
"""


class Singleton(type):
    _classes = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._classes:
            cls._classes[cls] = super().__call__(*args, **kwargs)
        return cls._classes[cls]
