# -*- coding: utf-8 -*-
from importlib import import_module


def create(config, *args, **kwargs):
    if config['mode'] == 'emulator':
        from .emulator import Emulator
        return Emulator(config, *args, **kwargs)

    if config['mode'] == 'physical':
        from .physical import Physical
        return Physical(config, *args, **kwargs)

    raise Exception("Unsupported mode")
