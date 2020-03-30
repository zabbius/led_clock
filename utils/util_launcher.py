# -*- coding: utf-8 -*-

import argparse
import json
import logging
import logging.config
import os
import sys
import traceback


class DummyUtil:
    def __init__(self, config):
        pass

    def run(self):
        pass


class UtilLauncher:
    def __init__(self):
        self.path = os.path.realpath(sys.argv[0])
        self.directory = os.path.dirname(self.path)
        self.logger = None
        pass

    def get_default_config_path(self):
        return self.directory + "/config.conf"

    def get_config_override_section(self, config):
        return config

    def add_arguments_to_parser(self, parser):
        pass

    def create_util(self, config):
        return DummyUtil(config)

    def run(self, change_dir=False):
        if change_dir:
            os.chdir(self.directory)

        parser = argparse.ArgumentParser()
        parser.add_argument("-c", "--config", default=self.get_default_config_path(), help="Config file location")

        self.add_arguments_to_parser(parser)

        args = vars(parser.parse_args())

        config = {}

        with open(args['config'], 'r') as config_file:
            config = json.load(config_file)

        log_config = config['Logging']
        log_config['version'] = 1
        logging.config.dictConfig(log_config)

        self.logger = logging.getLogger("Main")

        try:
            self.logger.info("New instance started with command line {0}".format(sys.argv))
            config = config['Settings']

            self.logger.info("Args is {0}".format(args))
            self.logger.info("Config is {0}".format(config))

            override = self.get_config_override_section(config)

            for (name, value) in args.items():
                if value is not None:
                    override[name] = value

            self.logger.info("Effective config is {0}".format(config))

            self.logger.info("Creating runnable")
            runnable = self.create_util(config)

            try:
                self.logger.info("Executing runnable")
                runnable.run()
            except Exception as ex:
                self.logger.error("Exception caught: {0}\n{1}".format(ex, traceback.format_exc()))

            self.logger.info("Instance ended")

        except Exception as ex:
            self.logger.error("Exception caught: {0}\n{1}".format(ex, traceback.format_exc()))
