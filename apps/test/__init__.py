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

    def enter(self):
        self.timer.start(True)

    def exit(self):
        self.timer.stop()

    def draw(self):
        image = Image.new('1', (self.width, self.height))
        canvas = ImageDraw.Draw(image)


        del canvas
        self.drawActivity(image)

    def on_timer(self):
        self.draw()

    def input(self, btn):
        if btn == InputButtons.BTN_STAR:
            self.close()
            return


def create(*args, **kwargs):
    return TestApp(*args, **kwargs)
