# -*- coding: utf-8 -*-

import datetime
import logging
import math

from PIL import Image, ImageDraw
from luma.core.legacy import text, textsize
from luma.core.legacy.font import LCD_FONT, proportional
from core import ClockFace
from utils import SafeTimer


class AnalogClock(ClockFace):
    def __init__(self, config, *args, **kwargs):
        super().__init__(config, *args, **kwargs)
        self.logger = logging.getLogger(__class__.__name__)

        self.timer = SafeTimer(self.on_timer, max(0.1, self.config.get('interval', 0)))
        self.font = proportional(LCD_FONT)

        self.size = min(self.width, self.height)

        if self.size % 2 == 0:
            self.size -= 1

        self.second_len = config.get('second_len', self.size / 2 - 2)
        self.minute_len = config.get('minute_len', self.size / 2 - 3)
        self.hour_len = config.get('hour_len', self.size / 2 - 5)

        self.background = None

    def start(self):

        self.background = Image.new('1', (self.size, self.size))

        canvas = ImageDraw.Draw(self.background)

        center = int(self.size / 2)

        for h in range(0, 12):
            x = center + int(math.sin(h * math.pi / 6) * self.size / 2)
            y = center - int(math.cos(h * math.pi / 6) * self.size / 2)
            canvas.point((x, y), 255)

        canvas.point((self.size / 2, 1), 255)
        canvas.point((self.size / 2, self.size - 2), 255)
        canvas.point((1, self.size / 2), 255)
        canvas.point((self.size - 2, self.size / 2), 255)

        del canvas

    def stop(self):
        self.background.close()
        self.background = None

    def enter(self):
        self.timer.start(True)

    def exit(self):
        self.timer.stop()

    def on_timer(self):
        now = datetime.datetime.now()

        seconds = now.second
        minutes = now.minute + seconds / 60.0
        hours = now.hour + minutes / 60.0

        if hours > 12:
            hours -= 12

        image = Image.new('1', (self.width, self.height))

        bg_x = int((self.width - self.background.width) / 2)
        bg_y = int((self.height - self.background.height) / 2)

        image.paste(self.background, (bg_x, bg_y))

        center_x = int(bg_x + self.background.width / 2)
        center_y = int(bg_y + self.background.height / 2)

        canvas = ImageDraw.Draw(image)

        arrow_len = self.background.width / 2

        hour_x = center_x + int(math.sin(hours * math.pi / 6) * self.hour_len)
        hour_y = center_y - int(math.cos(hours * math.pi / 6) * self.hour_len)

        minute_x = center_x + int(math.sin(minutes * math.pi / 30) * self.minute_len)
        minute_y = center_y - int(math.cos(minutes * math.pi / 30) * self.minute_len)

        second_x = center_x + int(math.sin(seconds * math.pi / 30) * self.second_len)
        second_y = center_y - int(math.cos(seconds * math.pi / 30) * self.second_len)

        canvas.line([center_x, center_y, hour_x, hour_y], 255)
        canvas.line([center_x, center_y, minute_x, minute_y], 255)

        if image.getpixel((second_x, second_y)):
            canvas.point([second_x, second_y], 0)
        else:
            canvas.point([second_x, second_y], 255)

        canvas.ellipse([center_x - 1, center_y - 1, center_x + 1, center_y + 1], 0)
        canvas.point([center_x, center_y], 255)
        del canvas
        self.manager.draw_activity(self, image)


def create(*args, **kwargs):
    return AnalogClock(*args, **kwargs)
