# -*- coding: utf-8 -*-

import logging

from luma.core.legacy import text, textsize
from luma.core.legacy.font import proportional

from clock_app import ClockApp
from fonts import BIG_FONT
from utils import SafeTimer

import datetime


class SimpleClock(ClockApp):
    def __init__(self, width, height, get_canvas, config):
        super().__init__(width, height, get_canvas, config)
        self.logger = logging.getLogger("SimpleClock")

        self.clock_y = 0
        self.clock_height = 7
        self.direction = 1

        self.timer = SafeTimer(self.on_timer, max(0.1, self.config.get('interval', 0)))

        self.font = [[0]] * (ord(':') + 1)

        for ch in range(ord('0'), ord('9') + 1):
            self.font[ch] = BIG_FONT[ch]

        self.font[ord('\t')] = [0x00, 0x00, 0x00, 0x00, 0x00]
        self.font[ord(':')] = [0x00, 0x22, 0x00, 0x00, 0x00]

    def enter(self):
        self.clock_y = 0
        self.clock_height = 7
        self.direction = 1
        self.timer.start(True)

    def exit(self):
        self.timer.stop()

    def on_timer(self):
        now = datetime.datetime.now()

        if now.microsecond > 500000:
            time_string = now.strftime("%H:%M")
        else:
            time_string = now.strftime("%H\t%M")

        x = (self.width - textsize(time_string, self.font)[0] + 1) / 2

        with self.get_canvas() as canvas:
            text(canvas, (x, self.clock_y), time_string, 255, self.font)

        self.clock_y += self.direction

        if self.clock_y == 0 or self.clock_y + self.clock_height == self.height:
            self.direction = -self.direction



