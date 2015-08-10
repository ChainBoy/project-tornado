# -*- coding:utf-8 -*-


# @version: 1.0
# @author: zhipeng zhang
# @date: '15-4-13'


from project_tornado.handler.base_handler import BaseHandler


class WelcomeHandler(BaseHandler):
    # @tornado.web.authenticated

    def get(self):
        user = self.get_argument("name", "")
        self.render('main.html', user=user, admin=True)

    def post(self, *args, **kwargs):
        self.write("welcome! ~")


if __name__ == "__main__":
    pass
