# -*- coding: utf-8 -*-

import threading
import traceback


class ThreadWorker:
    def __init__(self, name, logger, worker_done):
        self.name = name
        self.worker_done = worker_done
        self.logger = logger
        self.command = None
        self.thread = threading.Thread(target=self.thread_proc, name=self.name)
        self.thread.daemon = True

        self.stop_flag = False
        self.wait_lock = threading.Lock()
        self.handle_lock = threading.Lock()

    def __str__(self):
        return self.name

    def start(self):
        self.logger.debug("{0}: Starting worker".format(self))
        self.stop_flag = False

        self.wait_lock.acquire()
        self.thread.start()

        self.logger.debug("{0}: Worker started".format(self))

    def stop(self):
        self.logger.debug("{0}: Stopping worker".format(self))
        self.stop_flag = True
        self.wait_lock.release()
        self.thread.join()
        self.logger.debug("{0}: Worker stopped".format(self))

    def do(self, command):
        self.logger.debug("{0}: Scheduling {1}".format(self, command))
        with self.handle_lock:
            self.command = command
            self.wait_lock.release()

    def thread_proc(self):
        self.logger.debug("{0}: Thread proc started".format(self))
        while not self.stop_flag:
            self.logger.debug("{0}: Waiting for command".format(self))
            self.wait_lock.acquire()
            command = self.command
            self.command = None

            if command is None:
                continue

            self.logger.debug("{0}: Got {1}".format(self, command))

            with self.handle_lock:
                try:
                    self.logger.debug("{0}: Executing command {1}".format(self, command))
                    command.execute()
                    self.logger.debug("{0}: Executed {1}".format(self, command))
                except Exception as ex:
                    self.logger.warning("{0}: Exception caught: {1}\n{2}".format(self, ex, traceback.format_exc()))

            self.worker_done(self)
        self.logger.debug("{0}: Thread proc ended".format(self))
