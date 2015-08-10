# -*- coding:utf-8 -*-


# @version: 1.0
# @author:
# @date: '14-4-10'


import logging
import logging.config


class Logger():

    instance = None

    def __init__(self):
        self._logger = logging.getLogger()

    @staticmethod
    def get_instance():
        if not Logger.instance:
            Logger.instance = Logger()
        return Logger.instance

    def get_logger(self, logger_name=None):
        if logger_name:
            Logger.get_instance().get_logger(logger_name)
        else:
            Logger.get_instance().get_logger()

    @staticmethod
    def load_configure(configure_file_name):
        print configure_file_name
        logging.config.fileConfig(configure_file_name)

    @staticmethod
    def info(message, logger_name=None):
        if logger_name:
            Logger.get_instance().get_logger(logger_name).info(message)
        else:
            Logger.get_instance().get_logger().info(message)

    @staticmethod
    def debug(message, logger_name=None):
        if logger_name:
            Logger.get_instance().get_logger(logger_name).debug(message)
        else:
            Logger.get_instance().get_logger().debug(message)

    @staticmethod
    def error(message, logger_name=None):
        if logger_name:
            Logger.get_instance().get_logger(logger_name).error(message)
        else:
            Logger.get_instance().get_logger().error(message)


if __name__ == "__main__":
    pass
