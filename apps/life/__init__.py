# -*- coding: utf-8 -*-

import datetime
import logging
import random

import math
from PIL import Image, ImageDraw

from core import ClockApp, InputButtons
from utils import SafeTimer


class LifeApp(ClockApp):
    def __init__(self, config, *args, **kwargs):
        super().__init__(config, *args, **kwargs)
        self.logger = logging.getLogger(__class__.__name__)

        self.timer = SafeTimer(self.on_timer, max(0.1, self.config.get('interval', 0)))
        self.cells = None
        self.new_cells = None

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

    def on_timer(self):
        image = Image.new('1', (self.width, self.height))
        canvas = ImageDraw.Draw(image)

        anybody_alive = False

        for x in range(self.width):
            for y in range(self.height):
                canvas.point((x, y), self.cells[x][y])

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

        del canvas
        self.draw(image)

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


def create(*args, **kwargs):
    return LifeApp(*args, **kwargs)
