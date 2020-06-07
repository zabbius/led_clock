# -*- coding: utf-8 -*-

import logging


class ClockService:
    def __init__(self, config, manager):
        self.config = config

        self.get_info = lambda key: manager.get_info(self, key)
        self.set_info = lambda key, value: manager.set_info(self, key, value)

    def start(self):
        pass

    def stop(self):
        pass


