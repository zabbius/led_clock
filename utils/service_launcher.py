# -*- coding: utf-8 -*-

import signal
import time
import traceback

from .util_launcher import UtilLauncher


class DummyService:
    def __init__(self, config):
        pass

    def start(self):
        pass

    def stop(self):
        pass


class ServiceRunnable:
    def __init__(self, config, service_launcher):
        self.config = config
        self.logger = service_launcher.logger
        self.serverLauncher = service_launcher

        self.needStop = False

        def on_int(*a):
            self.needStop = True

        signal.signal(signal.SIGINT, on_int)
        signal.signal(signal.SIGTERM, on_int)

    def stop(self):
        self.logger.info("Manual stop requested")
        self.needStop = True

    def run(self):
        self.logger.info("Creating service")

        service = self.serverLauncher.create_service(self.config)

        self.needStop = False
        try:
            self.logger.info("Starting service")
            service.start()
            self.logger.info("Service started")

            while not self.needStop:
                self.serverLauncher.idle()

        except Exception as ex:
            self.logger.error("Exception caught: {0}\n{1}".format(ex, traceback.format_exc()))

            self.logger.info("Stopping service")

        service.stop()
        self.logger.info("Service stopped")


class ServiceLauncher(UtilLauncher):
    def __init__(self):
        UtilLauncher.__init__(self)
        self.runnable = None

    def create_service(self, config):
        return DummyService(config)

    def create_util(self, config):
        self.runnable = ServiceRunnable(config, self)
        return self.runnable

    def idle(self):
        time.sleep(0.1)

    def stop(self):
        if self.runnable:
            self.runnable.stop()

    def run(self, change_dir=True):
        UtilLauncher.run(self, change_dir)
