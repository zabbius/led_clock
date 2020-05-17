# -*- coding: utf-8 -*-

import logging


class ClockFace:
    def __init__(self, config, width, height, get_canvas):
        self.width = width
        self.height = height
        self.config = config
        self.get_canvas = get_canvas

    def start(self):
        pass

    def stop(self):
        pass

    def enter(self):
        pass

    def exit(self):
        pass
