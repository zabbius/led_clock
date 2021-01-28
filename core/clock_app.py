# -*- coding: utf-8 -*-

from . import InputButtons
from .clock_face import ClockFace


class ClockApp(ClockFace):
    def __init__(self, config, manager, *args, **kwargs):
        super().__init__(config, manager, *args, **kwargs)

    def input(self, btn):
        pass

    def receives_input(self):
        return True

    def overrides_exit(self):
        return False
