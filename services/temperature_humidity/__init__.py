# -*- coding: utf-8 -*-
from importlib import import_module


def create(config, *args, **kwargs):
    if config['mode'] == 'emulator':
        from .emulator import Emulator
        return Emulator(config, *args, **kwargs)

    if config['mode'] == 'si7021':
        from .si7021 import SI7021
        return SI7021(config, *args, **kwargs)

    raise Exception("Unsupported mode")
