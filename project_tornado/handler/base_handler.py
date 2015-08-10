# -*- coding:utf-8 -*-


# @version: 1.0
# @author: zhipeng zhang
# @date: '2015-04-07'

import base64
import logging

import simplejson
import tornado.web

from project_tornado.model.api_entity import ApiEntity, ENUM_ERROR_CODE


class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", '*')

    def pool(self):
        return self.application.pool

    def get(self, *args, **kwargs):
        self.write(simplejson.dumps(self._get_request_json()))

    def render(self, template_name, **kwargs):
        """
        重构render，所有的render都会默认传入当前cookie用户名.
        :param template_name:
        :param kwargs:
        :return:
        """
        if not kwargs.get('user'):
            try:
                kwargs['user'] = self.get_argument("user")
            except AttributeError:
                kwargs['user'] = ""
        super(BaseHandler, self).render(template_name, **kwargs)

    def set_value(self, key, value):
        if not hasattr(self, "_return_json"):
            self._return_json = ApiEntity()
        if key:
            exec ("self._return_json.%s = value" % str(key))

    def set_error(self, error_code=0):
        code = str(error_code)
        message = ENUM_ERROR_CODE.get(code, "UnKnown Error, Please message to Admin.")
        self.set_value("code", code)
        self.set_value("message", message)

    def set_message(self, message):
        self.set_value("message", message)

    def end_by_code(self, error_code):
        self.set_error(error_code)
        self.return_json()

    def return_json(self):
        self.set_value("", "")
        self.write("%s" % self._return_json)
        #self.write(self._return_json.to_json())
        # del ApiEntity
        # from project_tornado.model.api_entity import ApiEntity
        self.flush()
        self.finish()

    def get_argument(self, name, default="", strip=True, name_type=str):
        """
        重构get_argument，进行类型转化.
        :param name: key
        :param default: default value
        :param strip:
        :param name_type:key type. int? str? ..
        :return: 返回转化后的值.
        """
        result = super(BaseHandler, self).get_argument(name, default=default, strip=strip)
        if result == "": return default
        if name_type == str:
            return result
        e_str = "result = %s('%s')" % (name_type.__name__, result)
        try:
            exec (e_str)
        except (ValueError, TypeError, SyntaxError), e:
            logging.error('base_handler get argu:E:(%s). e_str:%s' % (e, e_str))
            result = default
        return result

    def _get_request_json(self, field_key="data"):
        "获取json格式的数据.已经转为dict"
        body_json = self.request.headers.get("data", "") or self.get_argument(field_key)
        try:
            body_dict = simplejson.loads(body_json)
            return body_dict

        except simplejson.JSONDecodeError:
            logging.error("body is not json data? &%s=%s" % (field_key, body_json))
            return {}
            # self.request.json = body_dict


    if __name__ == "__main__":
        pass
