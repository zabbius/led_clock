# -*- coding: utf-8 -*-
import logging
import random

from core.clock_service import ClockService
from utils import SafeTimer


class Emulator(ClockService):
    def __init__(self, config, *args, **kwargs):
        super().__init__(config, *args, **kwargs)
        self.logger = logging.getLogger(__class__.__name__)

        self.upper_temp = self.config['upper_temp']
        self.lower_temp = self.config['lower_temp']
        self.upper_hum = self.config['upper_hum']
        self.lower_hum = self.config['lower_hum']
        self.upper_press = self.config['upper_press']
        self.lower_press = self.config['lower_press']

        self.timer = SafeTimer(self.on_timer, max(1, self.config.get('interval', 0)))

    def start(self):
        self.logger.info("Starting")
        self.timer.start(True)
        self.logger.info("Started")

    def stop(self):
        self.logger.info("Stopping")
        self.timer.stop()
        self.logger.info("Stopped")

    def on_timer(self):
        temperature = random.randint(self.lower_temp, self.upper_temp)
        humidity = random.randint(self.lower_hum, self.upper_hum)
        pressure = random.randint(self.lower_press, self.upper_press)

        self.logger.debug("Temperature: {0},  Humidity: {1}, Pressure: {2}".format(temperature, humidity, pressure))

        self.set_info('temperature', temperature)
        self.set_info('humidity', humidity)
        self.set_info('pressure', pressure)
