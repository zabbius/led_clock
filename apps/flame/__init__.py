# -*- coding: utf-8 -*-

import datetime
import logging
import random

import math
from PIL import Image, ImageDraw

from components import ProgressBar
from core import ClockApp, InputButtons
from utils import SafeTimer


class FlameTestApp(ClockApp):
    def __init__(self, config, *args, **kwargs):
        super().__init__(config, *args, **kwargs)
        self.logger = logging.getLogger(__class__.__name__)

        self.timer = SafeTimer(self.on_timer, max(0.05, self.config.get('interval', 0)))

        self.minHotspots = self.config.get('min_hotspots', 2)
        self.maxHotspots = self.config.get('max_hotspots', 16)
        self.hotspotStep = self.config.get('hotspot_step', 2)
        self.hotspots = self.config.get('hotspots', 6)

        self.minValue = self.config.get('min_value', 20)
        self.maxValue = self.config.get('max_value', 200)
        self.valueStep = self.config.get('value_step', 2)
        self.value = self.config.get('value', 40)

        self.barDelay = self.config.get('bar_delay', 1.0)

        self.main_frame = [[0 for x in range(self.height + 2)] for y in range(self.width + 2)]
        self.back_frame = [[0 for x in range(self.height + 2)] for y in range(self.width + 2)]

        self.hotspotBar = ProgressBar(ProgressBar.HORIZONTAL, self.minHotspots, self.maxHotspots, self.hotspots, 4, (self.height - 8) / 2, self.width - 8, 8)
        self.valueBar = ProgressBar(ProgressBar.VERTICAL, self.minValue, self.maxValue, self.value,(self.width - 8) / 2, 2, 8, self.height - 4)

        self.visibleBar = None
        self.visibleBarTimestamp = None

    def place_spots(self):
        for n in range(self.hotspots):
            x = random.randrange(1, self.width + 1)
            self.main_frame[x][self.height] = self.value

    def move_frame(self):
        for x in range(1, self.width + 1):
            for y in range(1, self.height + 1):
                self.back_frame[x][y - 1] = (
                    self.main_frame[x - 1][y - 1] +
                    self.main_frame[x - 1][y    ] +
                    self.main_frame[x - 1][y + 1] +
                    self.main_frame[x    ][y - 1] +
                    self.main_frame[x    ][y    ] +
                    self.main_frame[x    ][y + 1] +
                    self.main_frame[x + 1][y - 1] +
                    self.main_frame[x + 1][y    ] +
                    self.main_frame[x + 1][y + 1]
                ) // 9

        for x in range(1, self.width + 1):
            self.back_frame[x][self.height] = 0

        tmp = self.main_frame
        self.main_frame = self.back_frame
        self.back_frame = tmp

    def enter(self):
        self.timer.start(True)

    def exit(self):
        self.timer.stop()

    def draw(self):
        image = Image.new('1', (self.width, self.height))
        canvas = ImageDraw.Draw(image)

        for x in range(self.width):
            for y in range(self.height):
                canvas.point((x, y), 255 if self.main_frame[x + 1][y] > 0 else 0)

        if (self.visibleBar is not None and self.visibleBarTimestamp is not None
                and (datetime.datetime.now() - self.visibleBarTimestamp).total_seconds() <= self.barDelay):
            self.visibleBar.draw(canvas)

        del canvas
        self.manager.draw_activity(self, image)

    def on_timer(self):
        self.place_spots()
        self.move_frame()
        self.draw()

    def input(self, btn):
        now = datetime.datetime.now()

        if btn == InputButtons.BTN_RIGHT:
            self.hotspots += self.hotspotStep
            self.visibleBar = self.hotspotBar
            self.visibleBarTimestamp = now

        if btn == InputButtons.BTN_LEFT:
            self.hotspots -= self.hotspotStep
            self.visibleBar = self.hotspotBar
            self.visibleBarTimestamp = now

        if btn == InputButtons.BTN_UP:
            self.value += self.valueStep
            self.visibleBar = self.valueBar
            self.visibleBarTimestamp = now

        if btn == InputButtons.BTN_DOWN:
            self.value -= self.valueStep
            self.visibleBar = self.valueBar
            self.visibleBarTimestamp = now

        self.value = min(self.value, self.maxValue)
        self.value = max(self.value, self.minValue)

        self.hotspots = min(self.hotspots, self.maxHotspots)
        self.hotspots = max(self.hotspots, self.minHotspots)

        self.valueBar.value = self.value
        self.hotspotBar.value = self.hotspots


def create(*args, **kwargs):
    return FlameTestApp(*args, **kwargs)
