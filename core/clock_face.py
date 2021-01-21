# -*- coding: utf-8 -*-

import logging

from .clock_service import ClockService


class ClockFace(ClockService):
    def __init__(self, config, manager, width, height):
        super().__init__(config, manager)
        self.width = width
        self.height = height

        self.drawActivity = lambda image: manager.draw_activity(self, image)

    def enter(self):
        pass

    def exit(self):
        pass

    def receives_input(self):
        return False



