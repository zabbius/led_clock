# -*- coding: utf-8 -*-

import logging


class ClockScreen:
    def __init__(self, config):
        self.logger = logging.getLogger(__class__.__name__)
        self.config = config

        self.width = config['width']
        self.height = config['height']
        self.mode = config['mode']

        self.device = None

    def start(self):
        self.logger.info("Starting")

        if self.mode == 'emulator':
            from luma.emulator.device import pygame
            self.device = pygame(self.width, self.height, 0, '1', "led_matrix")

        elif self.mode == 'max7219':
            from luma.core.interface.serial import spi, noop
            from luma.led_matrix.device import max7219

            serial = spi(port=1, device=0, gpio=noop())
            self.device = max7219(serial, self.width, self.height, block_orientation=self.config['orientation'])
            self.device.contrast(self.config.get('contrast', 0) << 4)
        else:
            raise Exception("Unsupported mode")
        self.logger.info("Started")

    def stop(self):
        self.logger.info("Stopping")
        if self.device is not None:
            self.device.cleanup()
            self.device = None
        self.logger.info("Stopped")

    def display_image(self, image):
        if self.device is not None:
            self.device.display(image)
