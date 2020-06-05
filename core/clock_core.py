# -*- coding: utf-8 -*-

import importlib.util
import logging
import os

from PIL import Image

from utils import SafeTimer
from . import InputButtons
from .clock_input import ClockInput
from .clock_screen import ClockScreen
from .constants import TransitionDirections


class ClockCore:
    def __init__(self, config, faces, apps):
        self.logger = logging.getLogger(__class__.__name__)
        self.config = config

        transition_interval = self.config['transition']['interval']
        self.transition_step = self.config['transition']['step']

        self.transition_timer = SafeTimer(self.on_transition_timer, transition_interval, 'transition')

        self.faces_config = faces
        self.apps_config = apps

        self.screen = ClockScreen(self.config['screen'])
        self.input = ClockInput(self.config['input'])

        self.input.on_input += self.on_input

        self.faces_path = config['plugins']['faces_path']
        self.apps_path = config['plugins']['apps_path']

        self.faces = {}
        self.apps = {}
        self.faces_index = []

        self.current_face_index = None

        self.current_activity = None

        self.primary_image = None
        self.secondary_image = None

        self.transition_direction = None
        self.primary_x = 0
        self.primary_y = 0

        self.load_clock_faces()

    def draw(self, image, activity):
        if activity != self.current_activity:
            return

        self.primary_image = image

        if self.transition_direction is None:
            self.screen.display_image(image)

    def load_clock_faces(self):
        self.logger.info("Loading faces")
        for (name, config) in self.faces_config.items():
            self.logger.debug("Loading {0}".format(name))
            spec = importlib.util.spec_from_file_location(name, os.path.join(self.faces_path, name, '__init__.py'))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            face = module.create(config, self.screen.width, self.screen.height, lambda image: self.draw(image, face))
            self.faces[name] = face
            self.faces_index.append(name)

        self.current_face_index = 0

    def on_input(self, btn):
        self.logger.debug("Got input: %s" % btn)

        if btn == InputButtons.BTN_SHARP:
            self.restart_screen()

        transition_direction = None

        if btn == InputButtons.BTN_LEFT:
            self.current_face_index -=1
            if self.current_face_index < 0:
                self.current_face_index = len(self.faces_index) - 1
            transition_direction = TransitionDirections.RIGHT

        if btn == InputButtons.BTN_RIGHT:
            self.current_face_index += 1
            if self.current_face_index >= len(self.faces_index):
                self.current_face_index = 0
            transition_direction = TransitionDirections.LEFT

        if btn == InputButtons.BTN_UP:
            self.current_face_index -=1
            if self.current_face_index < 0:
                self.current_face_index = len(self.faces_index) - 1
            transition_direction = TransitionDirections.DOWN

        if btn == InputButtons.BTN_DOWN:
            self.current_face_index += 1
            if self.current_face_index >= len(self.faces_index):
                self.current_face_index = 0
            transition_direction = TransitionDirections.UP

        self.change_activity(self.faces[self.faces_index[self.current_face_index]], transition_direction)

    def restart_screen(self):
        self.logger.info("Restarting screen")
        activity = self.current_activity
        self.current_activity.exit()
        self.current_activity = None

        self.transition_direction = None
        self.transition_timer.stop()

        self.screen.stop()
        self.screen.start()

        self.current_activity = activity
        self.current_activity.enter()

    def start(self):
        self.logger.info("Starting")

        self.screen.start()
        self.input.start()

        for (name, face) in self.faces.items():
            face.start()

        self.current_activity = self.faces[self.faces_index[self.current_face_index]]
        self.current_activity.enter()

        self.logger.info("Started")

    def stop(self):
        self.logger.info("Stopping")
        self.current_activity.exit()

        for (name, face) in self.faces.items():
            face.stop()

        self.input.stop()
        self.screen.stop()
        self.logger.info("Stopped")

    def change_activity(self, activity, transition_direction):
        self.current_activity.exit()
        self.current_activity = activity
        self.current_activity.enter()

        if transition_direction is None:
            return

        self.secondary_image = self.primary_image
        self.transition_direction = transition_direction

        self.primary_x = 0
        self.primary_y = 0

        if transition_direction == TransitionDirections.UP:
            self.primary_y = self.screen.height
        if transition_direction == TransitionDirections.DOWN:
            self.primary_y = -self.screen.height
        if transition_direction == TransitionDirections.LEFT:
            self.primary_x = self.screen.width
        if transition_direction == TransitionDirections.RIGHT:
            self.primary_x = -self.screen.width

        self.transition_timer.start()

    def on_transition_timer(self):
        if self.transition_direction is None:
            return

        if self.transition_direction == TransitionDirections.UP:
            self.primary_y -= self.transition_step
            if self.primary_y < 0:
                self.primary_y = 0
        if self.transition_direction == TransitionDirections.DOWN:
            self.primary_y += self.transition_step
            if self.primary_y > 0:
                self.primary_y = 0
        if self.transition_direction == TransitionDirections.LEFT:
            self.primary_x -= self.transition_step
            if self.primary_x < 0:
                self.primary_x = 0
        if self.transition_direction == TransitionDirections.RIGHT:
            self.primary_x += self.transition_step
            if self.primary_x > 0:
                self.primary_x = 0

        image = Image.new('1', (self.screen.width, self.screen.height))

        secondary_x = self.primary_x
        secondary_y = self.primary_y

        if secondary_x > 0:
            secondary_x -= self.screen.width
        elif secondary_x < 0:
            secondary_x += self.screen.width

        if secondary_y > 0:
            secondary_y -= self.screen.height
        elif secondary_y < 0:
            secondary_y += self.screen.height

        image.paste(self.secondary_image, (secondary_x, secondary_y))
        image.paste(self.primary_image, (self.primary_x, self.primary_y))

        self.screen.display_image(image)

        if self.primary_x == 0 and self.primary_y == 0:
            self.transition_timer.stop()
            self.secondary_image = None
            self.transition_direction = None
