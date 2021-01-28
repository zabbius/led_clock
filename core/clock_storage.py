# -*- coding: utf-8 -*-
import json
import logging
import threading
import os


class ClockStorage:
    def __init__(self, config):
        self.logger = logging.getLogger(__class__.__name__)
        self.config = config

        self.path = self.config['path']
        self.saveFile = "%s/save.json" % self.path
        self.saveFileTemp = "%s/save_temp.json" % self.path

        self.local_info = {}
        self.stored_info = {}

        self.info_lock = threading.Lock()

    def start(self):
        self.logger.info("Starting")
        os.makedirs(self.path, exist_ok=True)

        try:
            with open(self.saveFile, 'r') as fp:
                self.stored_info = json.load(fp)

        except Exception as ex:
            self.logger.warning("Exception caught while loading state: {0}".format(ex))

        self.local_info = self.stored_info.copy()
        self.logger.info("Started")

    def stop(self):
        self.logger.info("Stopping")
        self.local_info = {}
        self.logger.info("Stopped")

    def get_info(self, activity, key):
        with self.info_lock:
            return self.local_info.get(key)

    def set_info(self, activity, key, value, store=False):
        with self.info_lock:
            self.local_info[key] = value

            if store:
                self.stored_info[key] = value
                try:
                    with open(self.saveFileTemp, 'w') as fp:
                        json.dump(self.stored_info, fp)
                    os.replace(self.saveFileTemp, self.saveFile)

                except Exception as ex:
                    self.logger.warning("Exception caught while saving state: {0}".format(ex))
