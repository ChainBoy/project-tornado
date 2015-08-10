# -*- coding:utf-8 -*-


# @version: 1.0
# @author: zhipeng zhang
# @date: '15-4-13'

from project_tornado.handler.client.base_handler import BaseHandler


class ErrorHandler(BaseHandler):
    """
    404 等异常处理。
    """
    def get(self):
        self.write_error(404)

    def post(self, *args, **kwargs):
        self.write_error(404, **kwargs)

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.render("404.html")
        else:
            self.write(status_code)


if __name__ == "__main__":
    pass
