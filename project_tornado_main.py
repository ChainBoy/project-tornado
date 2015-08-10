# -*- coding:utf-8 -*-


# @version: 1.0
# @author: zhangzhipeng
# @date: '2015-04-07'


import os
import logging

from project_tornado.utils.environment import Environment
from project_tornado.server import Server


class ProjectTornadoServerMain():

    def __init__(self):
        Environment.get_instance().init_by_file_name(os.getcwd(), __file__)
        self._project_tornado = Server()

    def start(self):
        # config_path = os.getcwd() + '/conf/' + os.path.relpath(os.getcwdu(), '..') + '.xml'
        logging.info("project_tornado Server Starting...")
        self._project_tornado.run()
        logging.info("project_tornado Server Closed.")


if __name__ == "__main__":
    ProjectTornadoServerMain().start()
