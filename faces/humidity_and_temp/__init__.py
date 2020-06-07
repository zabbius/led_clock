# -*- coding: utf-8 -*-

import datetime
import logging

from PIL import Image, ImageDraw
from luma.core.legacy import text, textsize
from luma.core.legacy.font import LCD_FONT, proportional
from core import ClockFace
from utils import SafeTimer


class HumidityAndTemp(ClockFace):
    def __init__(self, config, *args, **kwargs):
        super().__init__(config, *args, **kwargs)
        self.logger = logging.getLogger(__class__.__name__)

        self.timer = SafeTimer(self.on_timer, max(1, self.config.get('interval', 0)))

        self.font = proportional(LCD_FONT)

    def enter(self):
        self.timer.start(True)

    def exit(self):
        self.timer.stop()

    def on_timer(self):
        temperature = self.get_info('temperature')
        humidity = self.get_info('humidity')

        image = Image.new('1', (self.width, self.height))
        canvas = ImageDraw.Draw(image)
        text(canvas, (0, 0), str(temperature), 255, self.font)
        text(canvas, (0, 8), str(humidity), 255, self.font)
        del canvas
        self.draw(image)


def create(*args, **kwargs):
    return HumidityAndTemp(*args, **kwargs)
