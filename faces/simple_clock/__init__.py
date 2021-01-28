# -*- coding: utf-8 -*-

import datetime
import logging

from PIL import Image, ImageDraw
from luma.core.legacy import text, textsize

from core import ClockFace
from shared.fonts import BIG_DIGITS
from utils import SafeTimer


class SimpleClock(ClockFace):
    def __init__(self, config, *args, **kwargs):
        super().__init__(config, *args, **kwargs)
        self.logger = logging.getLogger(__class__.__name__)

        self.clock_y = 0
        self.clock_height = 7
        self.direction = 1

        self.timer = SafeTimer(self.on_timer, max(0.1, self.config.get('interval', 0)))

        self.font = [[0]] * (ord(':') + 1)

        for ch in range(ord('0'), ord('9') + 1):
            self.font[ch] = BIG_DIGITS[ch]

        self.font[ord('\t')] = [0x00, 0x00, 0x00, 0x00, 0x00]
        self.font[ord(':')] = [0x00, 0x22, 0x00, 0x00, 0x00]

    def enter(self):
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

        image = Image.new('1', (self.width, self.height))
        canvas = ImageDraw.Draw(image)
        text(canvas, (x, self.clock_y), time_string, 255, self.font)
        del canvas
        self.manager.draw_activity(self, image)

        self.clock_y += self.direction

        if self.clock_y == 0 or self.clock_y + self.clock_height == self.height:
            self.direction = -self.direction


def create(*args, **kwargs):
    return SimpleClock(*args, **kwargs)
