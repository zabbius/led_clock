# -*- coding: utf-8 -*-
import logging
import time

import smbus

from core.clock_service import ClockService
from utils import SafeTimer


class SI7021(ClockService):
    def __init__(self, config, *args, **kwargs):
        super().__init__(config, *args, **kwargs)
        self.logger = logging.getLogger(__class__.__name__)

        self.address = config['address']

        self.timer = SafeTimer(self.on_timer, max(1, self.config.get('interval', 0)))
        self.bus = None

    def start(self):
        self.logger.info("Starting")
        self.bus = smbus.SMBus(0)
        self.timer.start(True)
        self.logger.info("Started")

    def stop(self):
        self.logger.info("Stopping")
        self.timer.stop()
        self.bus.close()
        self.bus = None
        self.logger.info("Stopped")

    def on_timer(self):
        self.bus.write_byte(self.address, 0xF5)
        time.sleep(0.3)

        data0 = self.bus.read_byte(self.address)
        data1 = self.bus.read_byte(self.address)

        humidity = round(((data0 * 256 + data1) * 125 / 65536.0) - 6)

        time.sleep(0.3)
        self.bus.write_byte(self.address, 0xF3)
        time.sleep(0.3)
        data0 = self.bus.read_byte(self.address)
        data1 = self.bus.read_byte(self.address)

        temperature = round(((data0 * 256 + data1) * 175.72 / 65536.0) - 46.85)

        self.logger.debug("Temperature: {0},  Humidity: {1}".format(temperature, humidity))

        self.set_info('temperature', temperature)
        self.set_info('humidity', humidity)
