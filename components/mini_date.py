# -*- coding: utf-8 -*-
import datetime

from luma.core.legacy import text

from shared.fonts import MICRO_LETTERS, ProportionalFont
from . import Drawable


class MiniDate(Drawable):
    def __init__(self, x, y):

        self.digits = MICRO_LETTERS[:(ord(':') + 1)]

        proportional = ProportionalFont(MICRO_LETTERS, 2)

        self.font = [x for x in ProportionalFont(MICRO_LETTERS, 2)]

        for n in range(ord('0'), ord('9') + 1):
            self.font[n] = MICRO_LETTERS[n]

        super().__init__(x, y, 17, 5)

    def draw(self, canvas):
        now = datetime.datetime.now()

        if now.second % 4 > 1:
            time_string = now.strftime(" %d.%m")
        else:
            time_string = now.strftime("%a").upper()

        text(canvas, (self.x, self.y), time_string, 255, self.font)
