# -*- coding:utf-8 -*-


# @version: 1.0
# @author: zhipeng zhang
# @date: '15-4-13'


from project_tornado.handler.client.base_handler import BaseHandler


class WelcomeHandler(BaseHandler):
    # @tornado.web.authenticated

    def get(self, *args, **kwargs):
        name = self.get_argument("name")
        if not name:
            self.end_by_code(10006)
        self.set_value("name", name)
        self.end_by_code(20011)

    def post(self, *args, **kwargs):
        self.write("welcome! ~")


if __name__ == "__main__":
    pass
