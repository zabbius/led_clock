# -*- coding: utf-8 -*-

import datetime
import logging
import random

import math
from PIL import Image, ImageDraw

from components.progress_bar import ProgressBar
from core import ClockApp, InputButtons
from utils import SafeTimer


class LifeApp(ClockApp):
    def __init__(self, config, *args, **kwargs):
        super().__init__(config, *args, **kwargs)
        self.logger = logging.getLogger(__class__.__name__)

        self.minInterval = self.config.get('min_interval', 0.1)
        self.maxInterval = self.config.get('max_interval', 1.0)
        self.intervalStep = self.config.get('interval_step', 0.1)

        self.intervalBarDelay = self.config.get('interval_bar_delay', 1.0)

        self.interval = self.config.get('interval', 0.3)

        self.interval = min(self.interval, self.maxInterval)
        self.interval = max(self.interval, self.minInterval)

        self.lastIntervalChange = None

        self.timer = SafeTimer(self.on_timer, self.interval)

        self.cells = None
        self.new_cells = None

        self.intervalBar = ProgressBar(-self.maxInterval, -self.minInterval, -self.interval, 4, (self.height - 8) / 2, self.width - 8, 8)

    def start(self):
        self.init_cells()

    def init_cells(self):
        self.cells = [[random.choice([0, 255]) for x in range(self.height)] for y in range(self.width)]
        self.new_cells = [[0 for x in range(self.height)] for y in range(self.width)]

    def enter(self):
        self.timer.start(True)

    def exit(self):
        self.timer.stop()

    def near(self, x, y, system=None):
        if system is None:
            system = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        count = 0
        for i in system:
            if self.cells[(x + i[0]) % self.width][(y + i[1]) % self.height]:
                count += 1
        return count

    def draw(self):
        image = Image.new('1', (self.width, self.height))
        canvas = ImageDraw.Draw(image)

        for x in range(self.width):
            for y in range(self.height):
                canvas.point((x, y), self.cells[x][y])

        if (self.lastIntervalChange is not None
                and (datetime.datetime.now() - self.lastIntervalChange).total_seconds() <= self.intervalBarDelay):
            self.intervalBar.draw(canvas)

        del canvas
        self.drawActivity(image)

    def on_timer(self):
        anybody_alive = False

        self.draw()

        for x in range(self.width):
            for y in range(self.height):
                if self.cells[x][y]:
                    if self.near(x, y) not in (2, 3):
                        self.new_cells[x][y] = 0
                    else:
                        self.new_cells[x][y] = 255
                        anybody_alive = True
                elif self.near(x, y) == 3:
                    self.new_cells[x][y] = 255
                    anybody_alive = True
                else:
                    self.new_cells[x][y] = 0

        tmp = self.cells
        self.cells = self.new_cells
        self.new_cells = tmp

        if not anybody_alive:
            self.init_cells()

    def input(self, btn):
        if btn == InputButtons.BTN_STAR:
            self.close()
            return

        if btn == InputButtons.BTN_OK:
            self.init_cells()

        interval_changed = False

        if btn == InputButtons.BTN_UP or btn == InputButtons.BTN_RIGHT:
            self.interval -= self.intervalStep
            interval_changed = True

        if btn == InputButtons.BTN_DOWN or btn == InputButtons.BTN_LEFT:
            self.interval += self.intervalStep
            interval_changed = True

        if interval_changed:
            self.interval = min(self.interval, self.maxInterval)
            self.interval = max(self.interval, self.minInterval)

            self.timer.interval = self.interval
            self.intervalBar.value = -self.interval

            self.lastIntervalChange = datetime.datetime.now()
            self.draw()


def create(*args, **kwargs):
    return LifeApp(*args, **kwargs)
