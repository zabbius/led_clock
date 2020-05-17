# -*- coding: utf-8 -*-

import logging

from PIL import ImageDraw


class ClockCanvas:
    def __init__(self, image, display_image):
        self.image = image
        self.display_image = display_image

    def __enter__(self):
        self.draw = ImageDraw.Draw(self.image)
        return self.draw

    def __exit__(self, type, value, traceback):
        if type is None:
            self.display_image(self.image)
        del self.draw
        return False
