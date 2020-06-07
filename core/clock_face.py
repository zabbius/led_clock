# -*- coding: utf-8 -*-

import logging

from .clock_service import ClockService


class ClockFace(ClockService):
    def __init__(self, config, manager, width, height):
        super().__init__(config, manager)
        self.width = width
        self.height = height

        self.draw = lambda image: manager.draw(self, image)

    def enter(self):
        pass

    def exit(self):
        pass



