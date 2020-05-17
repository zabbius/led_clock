# -*- coding: utf-8 -*-

import logging

from .clock_face import ClockFace


class ClockApp(ClockFace):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def input(self, key):
        pass
