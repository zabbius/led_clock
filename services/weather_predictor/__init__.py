# -*- coding: utf-8 -*-

import logging

from core import ClockService
from utils import SafeTimer


class WeatherPredictor(ClockService):
    def __init__(self, config, *args, **kwargs):
        super().__init__(config, *args, **kwargs)
        self.logger = logging.getLogger(__class__.__name__)

        self.timer = SafeTimer(self.on_timer, max(600, self.config.get('interval', 0)))
        self.approxSize = self.config.get('approx_size', 6)
        self.historySize = self.config.get('history_size', 144)

        self.deltaMin = self.config.get('delta_min', 250)
        self.deltaMax = self.config.get('delta_max', -250)


    def start(self):
        self.logger.info("Starting")
        self.timer.start(True)
        self.logger.info("Started")

    def stop(self):
        self.logger.info("Stopping")
        self.timer.stop()
        self.logger.info("Stopped")

    def get_rain_probability(self, pressure_points):
        sum_x = 0.0
        sum_y = 0.0
        sum_x2 = 0.0
        sum_xy = 0.0

        approx_size = len(pressure_points)

        for i in range(approx_size):
            sum_x += i
            sum_y += pressure_points[i]
            sum_x2 += i * i
            sum_xy += i * pressure_points[i]

        a = (approx_size * sum_xy - sum_x * sum_y) / (approx_size * sum_x2 - sum_x * sum_x) * approx_size
        rain = (a - self.deltaMin) * 2 / (self.deltaMax - self.deltaMin) - 1

        if rain < -1.0:
            rain = -1.0
        elif rain > 1.0:
            rain = 1.0

        return rain

    def on_timer(self):
        pressure = self.manager.get_info(self, 'pressure')

        pressure_history = self.manager.get_info(self, 'pressure_history')
        if not pressure_history:
            pressure_history = []

        pressure_history.append(pressure)

        while len(pressure_history) > self.historySize:
            pressure_history = pressure_history[1:]

        self.manager.set_info(self, 'pressure_history', pressure_history, True)

        approx_points = pressure_history[-self.approxSize:]

        while len(approx_points) < self.approxSize:
            approx_points.insert(0, approx_points[0])

        rain_probability = self.get_rain_probability(approx_points)

        self.manager.set_info(self, 'rain_probability', rain_probability)


def create(*args, **kwargs):
    return WeatherPredictor(*args, **kwargs)
