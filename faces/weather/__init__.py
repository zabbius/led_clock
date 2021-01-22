# -*- coding: utf-8 -*-

import datetime
import logging

from PIL import Image, ImageDraw
from luma.core.legacy import text, textsize
from luma.core.legacy.font import LCD_FONT, proportional
from core import ClockFace
from shared.fonts import MICRO_LETTERS, ProportionalFont
from utils import SafeTimer


class Weather(ClockFace):
    def __init__(self, config, *args, **kwargs):
        super().__init__(config, *args, **kwargs)
        self.logger = logging.getLogger(__class__.__name__)

        self.timer = SafeTimer(self.on_timer, max(1, self.config.get('interval', 0)))

        self.font = [x for x in ProportionalFont(MICRO_LETTERS, 2)]
        self.font[ord('\t')] = [0x00]

    def enter(self):
        self.timer.start(True)

    def exit(self):
        self.timer.stop()

    def on_timer(self):
        temperature = self.get_info('temperature')
        humidity = self.get_info('humidity')
        pressure = self.get_info('pressure')

        image = Image.new('1', (self.width, self.height))
        canvas = ImageDraw.Draw(image)

        text(canvas, (0, 0), "T: {0}".format(temperature), 255, self.font)
        text(canvas, (0, 6), "H: {0}".format(humidity), 255, self.font)
        text(canvas, (0, 12), "P: {0}".format(pressure), 255, self.font)

        del canvas
        self.drawActivity(image)


def create(*args, **kwargs):
    return Weather(*args, **kwargs)