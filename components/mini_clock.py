# -*- coding: utf-8 -*-
import datetime

from luma.core.legacy import text

from shared.fonts import MICRO_LETTERS, ProportionalFont
from . import Drawable


class MiniClock(Drawable):
    def __init__(self, x, y):

        self.clock_font = MICRO_LETTERS[:(ord(':') + 1)]

        proportional = ProportionalFont(MICRO_LETTERS, 2)

        self.clock_font[ord(':')] = proportional[ord(':')]
        self.clock_font[ord(' ')] = proportional[ord(' ')]

        super().__init__(x, y, 17, 5)

    def draw(self, canvas):
        now = datetime.datetime.now()

        if now.microsecond > 500000:
            time_string = now.strftime("%H:%M")
        else:
            time_string = now.strftime("%H %M")

        text(canvas, (self.x, self.y), time_string, 255, self.clock_font)
