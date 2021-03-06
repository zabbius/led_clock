#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from core.clock_core import ClockCore

if __name__ == "__main__":
    from utils import ServiceLauncher


    class Launcher(ServiceLauncher):
        def create_service(self, config):
            return ClockCore(config['Core'], config['Services'], config['Faces'], config['Apps'])

        def add_arguments_to_parser(self, parser):
            pass

    Launcher().run()
