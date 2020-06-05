# -*- coding: utf-8 -*-

import logging
import socket
import threading

from utils import MulticastDelegate


class ClockInput:
    def __init__(self, config):
        self.logger = logging.getLogger(__class__.__name__)
        self.config = config

        self.socket_path = config['socket']

        self.on_input = MulticastDelegate()
        self.socket = None

        self._stop = False
        self.thread = None

    def start(self):
        self.logger.info("Starting")

        self.logger.debug('Opening socket %s' % self.socket_path)
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.socket.connect(self.socket_path)
        self.socket.settimeout(0.1)

        self.thread = threading.Thread(target=self.thread_proc)
        self.thread.daemon = True
        self.thread.start()

        self.logger.info("Started")

    def stop(self):
        self.logger.info("Stopping")
        self._stop = True
        if self.thread is not None:
            self.thread.join()
            self.thread = None
        if self.socket:
            self.socket.close()
            self.socket = None

        self.logger.info("Stopped")

    def thread_proc(self):
        while not self._stop:
            try:
                data = self.socket.recv(128)
                data = data.strip()
                if data:
                    words = data.split()
                    self.on_input(words[2])

            except socket.timeout:
                pass