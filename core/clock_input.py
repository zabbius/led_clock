# -*- coding: utf-8 -*-

import logging
import threading
import time

from utils import MulticastDelegate


class ClockInput:
    def __init__(self, config):
        self.logger = logging.getLogger(__class__.__name__)
        self.config = config

        self.source = config['source']

        self.on_input = MulticastDelegate()
        self._stop = False
        self.thread = None

    def start(self):
        self.logger.info("Starting")

        if self.source == 'emulator':
            self.thread = threading.Thread(target=self.pygame_thread_proc)
            self.thread.daemon = True
        else:
            raise Exception("Unsupported device")

        self.thread.start()

        self.logger.info("Started")

    def stop(self):
        self.logger.info("Stopping")
        self._stop = True
        self.thread.join()
        self.logger.info("Stopped")

    def pygame_thread_proc(self):
        import pygame

        while not self._stop:
            time.sleep(1)
            #for event in pygame.event.get():
            #    self.logger.debug("Got pygame event {0}".fotmar(event))

