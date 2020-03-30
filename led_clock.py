#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from luma.core.render import canvas


from simple_clock import SimpleClock


class LedClock:
    def __init__(self, config):
        self.logger = logging.getLogger("LedClock")
        self.config = config

        self.screen = None
        self.create_screen(config['screen'])

        apps_config = config.get('apps', {})

        self.apps = [
            SimpleClock(self.screen.width, self.screen.height, self.get_canvas, apps_config.get("SimpleClock", {}))
        ]

        self.default_app = self.apps[0]

    def create_screen(self, config):
        if config['device'] == 'emulator':
            from luma.emulator.device import pygame
            self.screen = pygame(config['width'], config['height'], 0, '1', "led_matrix")

        elif config['device'] == 'max7219':
            from luma.core.interface.serial import spi, noop
            from luma.led_matrix.device import max7219

            serial = spi(port=1, device=0, gpio=noop())
            self.screen = max7219(serial, config['width'], config['height'], block_orientation=config['orientation'])
            self.screen.contrast(config.get('contrast', 0) << 4)
        else:
            raise Exception("Unsupported device")

    def get_canvas(self):
        return canvas(self.screen)

    def start(self):
        self.logger.info("Starting")
        for app in self.apps:
            app.start()
        self.logger.info("Started")

        self.default_app.enter()

    def stop(self):
        self.logger.info("Stopping")
        self.default_app.exit()

        for app in self.apps:
            app.stop()
        self.logger.info("Stopped")


if __name__ == "__main__":
    from utils import ServiceLauncher


    class Launcher(ServiceLauncher):
        def create_service(self, config):
            return LedClock(config['LedClock'])

        def add_arguments_to_parser(self, parser):
            pass

    Launcher().run()
