# -*- coding:utf-8 -*-


# @version: 1.0
# @author: zhipeng zhang
# @date: '15-04-07'

import logging

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
from tornado.options import define

from application import Application
from configure.configure import configure

DEFAULT_PORT = 8000
DEFAULT_ADDRESS = "0.0.0.0"


class Server(object):
    def __init__(self):
        self._load_config()

    def _load_config(self):
        application_config = configure.get_application_setting()
        self.address = application_config.get('address', DEFAULT_ADDRESS)
        try:
            self.port = int(application_config.get('port', DEFAULT_PORT))
        except ValueError:
            self.port = DEFAULT_PORT
        self.application_config = application_config

    #@staticmethod
    def run(self):
        tornado.options.parse_command_line()
        application = Application(self.application_config, configure)
        http_server = tornado.httpserver.HTTPServer(application, xheaders=True)
        http_server.listen(self.port, address=self.address)
        try:
            logging.info('Start:http://127.0.0.1:%s' % self.port)
            tornado.ioloop.IOLoop.instance().start()
        except KeyboardInterrupt:
            logging.info("Keyboard end Server.")


if __name__ == "__main__":
    Server().run()
