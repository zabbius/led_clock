# -*- coding: utf-8 -*-

import importlib.util
import logging
import threading

from PIL import Image

from utils import SafeTimer
from .clock_input import ClockInput
from .clock_screen import ClockScreen
from .clock_storage import ClockStorage

from .constants import InputButtons, TransitionDirections
from .input_utils import InputUtils


class ClockCore:
    def __init__(self, config, services_config, faces_config, apps_config):
        self.logger = logging.getLogger(__class__.__name__)
        self.config = config

        transition_interval = self.config['transition']['interval']
        self.transition_step = self.config['transition']['step']

        self.transition_timer = SafeTimer(self.on_transition_timer, transition_interval, 'transition')

        self.screen = ClockScreen(self.config['screen'])
        self.input = ClockInput(self.config['input'])
        self.storage = ClockStorage(self.config['storage'])

        self.input.on_input += self.on_input

        self.services = []
        self.faces = []
        self.apps = []

        self.current_activity = None

        self.primary_image = None
        self.secondary_image = None

        self.transition_direction = None
        self.primary_x = 0
        self.primary_y = 0

        self.logger.info("Loading services")
        self.services = self.load_plugins(services_config, "services",
                                          lambda create, name, conf: create(conf, self))
        self.logger.info("Loading faces")
        self.faces = self.load_plugins(faces_config, "faces",
                                       lambda create, name, conf: create(conf, self, self.screen.width, self.screen.height))
        self.logger.info("Loading apps")
        self.apps = self.load_plugins(apps_config, "apps",
                                      lambda create, name, conf: create(conf, self, self.screen.width, self.screen.height))

        self.current_face_index = 0

    def get_info(self, activity, key):
        return self.storage.get_info(activity, key)

    def set_info(self, activity, key, value, store=False):
        self.storage.set_info(activity, key, value, store)

    def draw_activity(self, activity, image):
        if activity != self.current_activity:
            return

        self.primary_image = image

        if self.transition_direction is None:
            self.screen.display_image(image)

    def load_plugins(self, plugins, plugin_folder, factory):
        result = []
        for (name, config) in plugins.items():
            if not config.get("enabled", True):
                continue

            self.logger.debug("Loading {0}".format(name))
            module = importlib.import_module("%s.%s" % (plugin_folder, name))
            result.append(factory(module.create, name, config))

        return result

    def on_input(self, btn):
        self.logger.debug("Got input: %s" % btn)

        if btn == InputButtons.BTN_SHARP:
            self.restart_screen()

        if self.current_activity.receives_input():
            if not self.current_activity.overrides_exit() and btn == InputButtons.BTN_STAR:
                self.close_app(self.current_activity)
            else:
                self.current_activity.input(btn)
            return

        app = None

        try:
            app_index = InputUtils.NumericButtonsSequence.index(btn)
            app = self.apps[app_index]

        except IndexError:
            pass
        except ValueError:
            pass

        if app is not None:
            self.open_app(app)
            return

        transition_direction = None

        if btn == InputButtons.BTN_LEFT:
            self.current_face_index -= 1
            if self.current_face_index < 0:
                self.current_face_index = len(self.faces) - 1
            transition_direction = TransitionDirections.RIGHT

        if btn == InputButtons.BTN_RIGHT:
            self.current_face_index += 1
            if self.current_face_index >= len(self.faces):
                self.current_face_index = 0
            transition_direction = TransitionDirections.LEFT

        if btn == InputButtons.BTN_UP:
            self.current_face_index -= 1
            if self.current_face_index < 0:
                self.current_face_index = len(self.faces) - 1
            transition_direction = TransitionDirections.DOWN

        if btn == InputButtons.BTN_DOWN:
            self.current_face_index += 1
            if self.current_face_index >= len(self.faces):
                self.current_face_index = 0
            transition_direction = TransitionDirections.UP

        self.change_activity(self.faces[self.current_face_index], transition_direction)

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
        self.storage.start()

        for plugin in self.services:
            plugin.start()
        for plugin in self.faces:
            plugin.start()
        for plugin in self.apps:
            plugin.start()

        self.current_activity = self.faces[self.current_face_index]
        self.current_activity.enter()

        self.logger.info("Started")

    def stop(self):
        self.logger.info("Stopping")
        self.current_activity.exit()

        for plugin in self.apps:
            plugin.stop()
        for plugin in self.faces:
            plugin.stop()
        for plugin in self.services:
            plugin.stop()

        self.storage.stop()
        self.input.stop()
        self.screen.stop()
        self.logger.info("Stopped")

    def open_app(self, app):
        self.change_activity(app, TransitionDirections.LEFT)

    def close_app(self, app):
        if app != self.current_activity:
            return

        self.change_activity(self.faces[self.current_face_index], TransitionDirections.RIGHT)

    def change_activity(self, activity, transition_direction):
        self.current_activity.exit()
        self.transition_direction = transition_direction
        current_image = self.primary_image

        self.current_activity = activity
        self.current_activity.enter()

        if transition_direction is None:
            return

        self.secondary_image = current_image

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
