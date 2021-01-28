# -*- coding: utf-8 -*-
import logging
import time

from smbus import SMBus
from si7021 import Si7021
from .bme280 import Bme280

from core import ClockService
from utils import SafeTimer


class Physical(ClockService):
    def __init__(self, config, *args, **kwargs):
        super().__init__(config, *args, **kwargs)
        self.logger = logging.getLogger(__class__.__name__)

        self.busNumber = config.get('smbus', 0)
        self.timer = SafeTimer(self.on_timer, max(1, self.config.get('interval', 0)))
        self.measureCycles = config.get('measure_cycles', 10)

        self.smbus = None
    def start(self):

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

    def measure(self):
        hum1, temp1 = self.si7021.read()
        hum2, temp2, pres2 = self.bme208.read()

        temperature = (temp1 + temp2) / 2
        pressure = pres2
        humidity = hum1

        return temperature, pressure, humidity

    def on_timer(self):
        temperature = 0
        pressure = 0
        humidity = 0

        for n in range(self.measureCycles):
            t, p, h = self.measure()
            temperature += t
            pressure += p
            humidity += h
            time.sleep(0.001)

        temperature /= self.measureCycles
        pressure /= self.measureCycles
        humidity /= self.measureCycles

        self.logger.debug("Temperature: {0},  Humidity: {1}, Pressure: {2}".format(temperature, humidity, pressure))
        self.manager.set_info(self, 'temperature', temperature)
        self.manager.set_info(self, 'humidity', humidity)
        self.manager.set_info(self, 'pressure', pressure)
