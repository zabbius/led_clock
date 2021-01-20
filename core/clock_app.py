# -*- coding: utf-8 -*-

from . import InputButtons
from .clock_face import ClockFace


class ClockApp(ClockFace):
    def __init__(self, config, manager, *args, **kwargs):
        super().__init__(config, manager, *args, **kwargs)

        self.close = lambda: manager.close_app(self)

    def input(self, btn):
        if btn == InputButtons.BTN_STAR:
            self.close()
            return True

    def receives_input(self):
        return True
