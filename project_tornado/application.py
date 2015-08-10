# -*- coding:utf-8 -*-


# @version: 1.0
# @author: zhipeng zhang
# @date: '15-04-07'

import os

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define

from project_tornado.handler.client import Client
from project_tornado.handler.welcome_handler import WelcomeHandler, BaseHandler


define("debug", default=True, type=bool)
define("cookie", default="0.0.0.044.154+9556+5sdf465", type=str)
define("static_path", default=os.path.join(
    os.path.dirname(__file__), "static"), type=str)
define("template_path", default=os.path.join(
    os.path.dirname(__file__), "template"), type=str)


class Application(tornado.web.Application):

    def __init__(self, settings, configure):
        settings["configure"] = configure
        handlers = [
            (r'/static/(.*)', tornado.web.StaticFileHandler,
             {'path': settings.get("static_path")}),
            (r'/client/files/(.*)', tornado.web.StaticFileHandler,
             {'path': settings.get("files_dir")}),
            (r'/(favicon.ico)', tornado.web.StaticFileHandler, {"path": ""}),


            # -------- client  -----------
            (r"/client/welcome/?$", Client.WelcomeHandler),

            # -------- client  -----------

            (r"/welcome/?$", WelcomeHandler),
            (r"/?$", BaseHandler),

            (r'.*', Client.ErrorHandler),
        ]
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == "__main__":
    pass
