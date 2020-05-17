# -*- coding: utf-8 -*-

import logging
import importlib.util
import os

from .clock_input import ClockInput
from .clock_screen import ClockScreen


class ClockCore:
    def __init__(self, config, faces, apps):
        self.logger = logging.getLogger(__class__.__name__)
        self.config = config

        self.faces_config = faces
        self.apps_config = apps

        self.screen = ClockScreen(self.config['screen'])
        self.input = ClockInput(self.config['input'])

        self.faces_path = config['plugins']['faces_path']
        self.apps_path = config['plugins']['apps_path']

        self.faces = {}
        self.current_face = None

        self.apps = {}
        self.current_app = None

        self.load_clock_faces()

    def load_clock_faces(self):
        self.logger.info("Loading faces")
        for (name, config) in self.faces_config.items():
            self.logger.debug("Loading {0}".format(name))
            spec = importlib.util.spec_from_file_location(name, os.path.join(self.faces_path, name, '__init__.py'))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            face = module.create(config, self.screen.width, self.screen.height, self.screen.get_canvas)
            self.faces[name] = face

            if self.current_face is None:
                self.current_face = face

    def start(self):
        self.logger.info("Starting")
        self.screen.start()
        self.input.start()

        for (name, face) in self.faces.items():
            face.start()

        self.current_face.enter()
        self.logger.info("Started")

    def stop(self):
        self.logger.info("Stopping")

        self.current_face.exit()

        for (name, face) in self.faces.items():
            face.stop()

        self.input.stop()
        self.screen.stop()
        self.logger.info("Stopped")

