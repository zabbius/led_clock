# -*- coding: utf-8 -*-

import datetime
import logging
import random

from PIL import Image, ImageDraw
from luma.core.legacy import text, textsize

from core import ClockApp, InputButtons, InputUtils
from shared.fonts import MICRO_LETTERS, ProportionalFont

from utils import SafeTimer


class SnakeApp(ClockApp):
    def __init__(self, config, *args, **kwargs):
        super().__init__(config, *args, **kwargs)
        self.logger = logging.getLogger(__class__.__name__)

        self.minInterval = self.config.get('min_interval', 0.1)
        self.maxInterval = self.config.get('max_interval', 1.0)

        self.intervalStep = (self.maxInterval - self.minInterval) / 9
        self.level = 5

        self.timer = SafeTimer(self.on_timer, self.maxInterval - self.intervalStep * self.level)

        self.snake = None
        self.dx = 0
        self.dy = 0
        self.apple = None
        self.score = 0
        self.gameOver = False

        self.btn = None

        self.gameWidth = self.width
        self.gameHeight = self.height - 6

        self.main_font = [x for x in ProportionalFont(MICRO_LETTERS, 2)]
        self.main_font[ord('\t')] = [0x00]

        self.clock_font = MICRO_LETTERS[:(ord(':') + 1)]
        self.clock_font[ord(':')] = self.main_font[ord(':')]
        self.clock_font[ord(' ')] = self.main_font[ord(' ')]

    def start(self):
        self.init_game()

    def gen_apple_pos(self):
        while True:
            x, y = random.randrange(self.gameWidth), random.randrange(self.gameHeight)
            if (x, y) not in self.snake:
                return x, y

    def init_game(self):
        self.snake = [
            (int(self.gameWidth / 2) - 1, int(self.gameHeight / 2)),
            (int(self.gameWidth / 2), int(self.gameHeight / 2)),
            (int(self.gameWidth / 2) + 1, int(self.gameHeight / 2))
        ]

        self.score = 0

        self.dx = 1
        self.dy = 0
        self.apple = self.gen_apple_pos()

        self.gameOver = False
        self.btn = None

    def get_next_pos(self):
        x, y = self.snake[-1]
        x += self.dx
        y += self.dy

        if x >= self.gameWidth:
            x = 0
        if x < 0:
            x = self.gameWidth - 1
        if y >= self.gameHeight:
            y = 0
        if y < 0:
            y = self.gameHeight - 1

        return x, y

    def enter(self):
        self.timer.start(True)

    def exit(self):
        self.timer.stop()

    def draw(self):
        image = Image.new('1', (self.width, self.height))
        canvas = ImageDraw.Draw(image)

        now = datetime.datetime.now()

        if now.microsecond > 500000:
            time_string = now.strftime("%H:%M")
        else:
            time_string = now.strftime("%H %M")

        time_width = textsize(time_string, self.clock_font)[0]
        text(canvas, (self.width - time_width + 1, 0), time_string, 255, self.clock_font)

        text(canvas, (0, 0), str(self.score), 255, self.main_font)

        canvas.point((self.apple[0], self.apple[1] + 6), 255)
        for x, y in self.snake:
            canvas.point((x, y + 6), 255)

        if self.gameOver:
            canvas.rectangle((0, 13, self.width, 19), 0, 0)
            text(canvas, (0, 14), "GAME\tOVER", 255, self.main_font)

        del canvas
        self.drawActivity(image)

    def on_timer(self):
        if self.gameOver:
            self.draw()
            return

        if self.btn == InputButtons.BTN_UP and self.dx != 0:
            self.dx = 0
            self.dy = -1
        if self.btn == InputButtons.BTN_DOWN and self.dx != 0:
            self.dx = 0
            self.dy = 1
        if self.btn == InputButtons.BTN_LEFT and self.dy != 0:
            self.dx = -1
            self.dy = 0
        if self.btn == InputButtons.BTN_RIGHT and self.dy != 0:
            self.dx = 1
            self.dy = 0

        next_pos = self.get_next_pos()

        if next_pos in self.snake:
            self.gameOver = True
        else:
            self.snake.append(next_pos)

            if next_pos != self.apple:
                self.snake = self.snake[1:]
            else:
                self.score += self.level + 1
                self.apple = self.gen_apple_pos()

        self.draw()

    def input(self, btn):
        if btn == InputButtons.BTN_STAR:
            self.close()
            return

        if btn == InputButtons.BTN_OK:
            self.init_game()
            return

        if btn == InputButtons.BTN_0:
            return

        index = InputUtils.get_numeric_button_index(btn)

        if index is not None:
            self.level = index
            self.timer.interval = self.maxInterval - self.intervalStep * self.level
            return

        self.btn = btn


def create(*args, **kwargs):
    return SnakeApp(*args, **kwargs)
