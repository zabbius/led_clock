# -*- coding: utf-8 -*-

import logging
from queue import Queue, Full, Empty

from .thread_worker import ThreadWorker


class MultiThreadingDispatcher:
    def __init__(self, name, threads_number, max_queue_size=0):
        self.name = name
        self.threads_number = threads_number
        self.max_queue_size = max_queue_size
        self.commands_queue = Queue(self.max_queue_size)

        self.workers_queue = Queue()
        self.free_workers_queue = Queue()
        self.logger = logging.getLogger("MultiThreadingDispatcher")

    def __str__(self):
        return self.name

    def start(self):
        self.logger.debug("{0}: Starting dispatcher".format(self))
        for n in range(self.threads_number):
            worker = ThreadWorker("{0} Worker #{1}".format(self, n), self.logger, self.__worker_done)
            worker.start()
            self.workers_queue.put(worker)
            self.__worker_done(worker)
        self.logger.debug("{0}: Dispatcher started".format(self))

    def stop(self):
        self.logger.debug("{0}: Stopping dispatcher".format(self))
        while True:
            try:
                worker = self.workers_queue.get_nowait()
                worker.stop()
            except Empty:
                break
        self.logger.debug("{0}: Dispatcher stopped".format(self))

    def dispatch(self, command):
        self.logger.debug("{0}: Dispatching command {1}".format(self, command))
        try:
            worker = self.free_workers_queue.get_nowait()
            worker.do(command)
        except Empty:
            try:
                self.logger.debug("{0}: All workers are busy, enqueueing {1}".format(self, command))
                self.commands_queue.put_nowait(command)
            except Full:
                self.logger.warning("{0}: Command queue is full, dropping {1}".format(self, command))
            self.logger.debug("{0}: Command queue size: {1}, Free workers: {2}".format(self, self.commands_queue.qsize(), self.free_workers_queue.qsize()))

    def __worker_done(self, worker):
        self.logger.debug("{0}: Worker {1} is done".format(self, worker))
        try:
            command = self.commands_queue.get_nowait()
            worker.do(command)
        except Empty:
            self.logger.debug("{0}: Worker {1} is free now".format(self, worker))
            self.free_workers_queue.put(worker)
        self.logger.debug("{0}: Command queue size: {1}, Free workers: {2}".format(self, self.commands_queue.qsize(), self.free_workers_queue.qsize()))
