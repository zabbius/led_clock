# -*- coding: utf-8 -*-

import datetime
import logging

import math
from PIL import Image, ImageDraw

from core import ClockApp, InputButtons
from utils import SafeTimer


class TestApp(ClockApp):
    def __init__(self, config, *args, **kwargs):
        super().__init__(config, *args, **kwargs)
        self.logger = logging.getLogger(__class__.__name__)

        self.timer = SafeTimer(self.on_timer, max(0.1, self.config.get('interval', 0)))

        self.x = self.width / 2
        self.y = self.height / 2

    def enter(self):
        self.timer.start(True)

    def exit(self):
        self.timer.stop()

    def on_timer(self):
        image = Image.new('1', (self.width, self.height))
        canvas = ImageDraw.Draw(image)
        canvas.point((self.x, self.y), 255)
        del canvas
        self.draw(image)

    def input(self, btn):
        if btn == InputButtons.BTN_STAR:
            self.close()
            return

        if btn == InputButtons.BTN_LEFT:
            self.x -= 1

        if btn == InputButtons.BTN_RIGHT:
            self.x += 1

        if btn == InputButtons.BTN_UP:
            self.y -= 1

        if btn == InputButtons.BTN_DOWN:
            self.y += 1

        if self.x < 0:
            self.x = self.width - 1
        if self.x >= self.width:
            self.x = 0

        if self.y < 0:
            self.y = self.height - 1
        if self.y >= self.height:
            self.y = 0


def create(*args, **kwargs):
    return TestApp(*args, **kwargs)
