# -*- coding: utf-8 -*-
import logging

from smbus import SMBus
from si7021 import Si7021
from .bme280 import Bme280

from core.clock_service import ClockService
from utils import SafeTimer


class Physical(ClockService):
    def __init__(self, config, *args, **kwargs):
        super().__init__(config, *args, **kwargs)
        self.logger = logging.getLogger(__class__.__name__)

        self.busNumber = config['bus']
        self.timer = SafeTimer(self.on_timer, max(1, self.config.get('interval', 0)))

        self.smbus = None
        self.si7021 = None
        self.bme208 = None

    def start(self):
        self.logger.info("Starting")
        self.smbus = SMBus(self.busNumber)
        self.si7021 = Si7021(self.smbus)
        self.si7021.reset()

        self.bme208 = Bme280(self.smbus)
        self.bme208.setup()

        self.timer.start(True)
        self.logger.info("Started")

    def stop(self):
        self.logger.info("Stopping")
        self.timer.stop()
        self.smbus.close()
        self.smbus = None
        self.logger.info("Stopped")

    def on_timer(self):
        hum1, temp1 = self.si7021.read()
        hum2, temp2, pres2 = self.bme208.read()

        temperature = (temp1 + temp2) / 2
        pressure = pres2
        humidity = hum1

        self.logger.debug("Temperature: {0},  Humidity: {1}, Pressure: {2}".format(temperature, humidity, pressure))
        self.set_info('temperature', temperature)
        self.set_info('humidity', humidity)
        self.set_info('pressure', pressure)
