# -*- coding: utf-8 -*-
from . import Drawable


class ProgressBar(Drawable):
    VERTICAL = 'vert'
    HORIZONTAL = 'horz'

    def __init__(self, kind, min_value, max_value, value, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.min = min_value
        self.max = max_value
        self.value = value
        self.kind = kind

    def draw(self, canvas):
        if self.kind == ProgressBar.HORIZONTAL:
            return self.draw_horz(canvas)

        if self.kind == ProgressBar.VERTICAL:
            return self.draw_vert(canvas)

    def draw_vert(self, canvas):
        value_height = (self.height - 4) * (self.value - self.min) / (self.max - self.min)

        if value_height > self.height - 4:
            value_height = self.height - 4
        if value_height < 1:
            value_height = 1

        canvas.rectangle((self.x, self.y, self.x + self.width - 1, self.y + self.height - 1), 0, 255)
        canvas.rectangle((self.x + 2, self.y + self.height - 2 - value_height, self.x + self.width - 3, self.y + self.height - 3), 255, 255)

    def draw_horz(self, canvas):
        value_width = (self.width - 4) * (self.value - self.min) / (self.max - self.min)

        if value_width > self.width - 4:
            value_width = self.width - 4
        if value_width < 1:
            value_width = 1

        canvas.rectangle((self.x, self.y, self.x + self.width - 1, self.y + self.height - 1), 0, 255)
        canvas.rectangle((self.x + 2, self.y + 2, self.x + 1 + value_width, self.y + self.height - 3), 255, 255)
