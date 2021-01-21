# -*- coding: utf-8 -*-
from . import Drawable


class ProgressBar(Drawable):
    def __init__(self, min_value, max_value, value, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.min = min_value
        self.max = max_value
        self.value = value

    def draw(self, canvas):
        value_width = (self.width - 4) * (self.value - self.min) / (self.max - self.min)

        if value_width > self.width - 4:
            value_width = self.width - 4
        if value_width < 0:
            value_width = 0

        canvas.rectangle((self.x, self.y, self.x + self.width, self.y + self.height - 1), 0, 255)
        canvas.rectangle((self.x + 2, self.y + 2, self.x + 2 + value_width, self.y + self.height - 3), 255, 255)
