# -*- coding: utf-8 -*-

import logging

from PIL import Image

from core.clock_canvas import ClockCanvas


class ClockScreen:
    def __init__(self, config):
        self.logger = logging.getLogger(__class__.__name__)
        self.config = config

        self.width = config['width']
        self.height = config['height']
        self.device = config['device']

        self.screen = None

    def start(self):
        self.logger.info("Starting")

        if self.device == 'emulator':
            from luma.emulator.device import pygame
            self.screen = pygame(self.width, self.height, 0, '1', "led_matrix")

        elif self.device == 'max7219':
            from luma.core.interface.serial import spi, noop
            from luma.led_matrix.device import max7219

            serial = spi(port=1, device=0, gpio=noop())
            self.screen = max7219(serial, self.width, self.height, block_orientation=self.config['orientation'])
            self.screen.contrast(self.config.get('contrast', 0) << 4)
        else:
            raise Exception("Unsupported device")
        self.logger.info("Started")

    def stop(self):
        self.logger.info("Stopping")
        if self.screen is not None:
            self.screen.cleanup()
            self.screen = None
        self.logger.info("Stopped")

    def create_image(self):
        if self.screen is None:
            return None
        return Image.new(self.screen.mode, self.screen.size)

    def display_image(self, image):
        if self.screen is None:
            return
        self.screen.display(image)

    def get_canvas(self):
        return ClockCanvas(self.create_image(), self.display_image)
