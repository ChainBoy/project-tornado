# -*- coding:utf-8 -*-


# @version: 1.0
# @author: Zhipeng Zhang
# @date: '2015/4/13'

import logging

from project_tornado.utils.compressor import Compressor
from project_tornado.utils.md5_checker import Md5Checker
from project_tornado.utils.mysql_helper import MysqlHelper


compressor = Compressor()
md5_checker = Md5Checker()

CLIENT_NOT_FIND = -1
CLIENT_CREATE_ERROR = -1

CLIENT_LOGGING = 1
CLIENT_UNLOGGING = 0

CLIENT_PASS = 1
CLIENT_UNPASS = 0

class ClientBal(object):
    def __init__(self, table_name="clients", db_conf={}):
        self._table_name = table_name
        self._db_conf = db_conf
        self._mysql = MysqlHelper(**db_conf)

    def create(self, client_name):
        "创建客户端"
        client_id = self.get_client_id_by_name(client_name)
        if client_id:
            return client_id
        else:
            sql = "INSERT INTO `%s` (`name`) VALUES ('%s');" % (self._table_name, client_name)
            client_count = self._mysql.insert(sql)
            if client_count > 0:
                client_id = self.get_client_id_by_name(client_name)
                if client_id:
                    return client_id
                #"创建失败(查找失败)"
                return CLIENT_CREATE_ERROR
            else:
                #"创建失败(插入失败)"
                return CLIENT_CREATE_ERROR

    def update_info(self, client):
        sql = "UPDATE " + self._table_name +" SET cpu=%(cpu)s, mem_us=%(mem_us)s, mem_all=%(mem_all)s, speed_rx=%(speed_rx)s, speed_expect=%(speed_expect)s, driver_us=%(driver_us)s, driver_all=%(driver_us)s WHERE  id=%(client_id)s;"
        return self._mysql.update(sql, client)

    def login(self, client_id, client_name):
        "客户端登录"
        client = self.get_client(client_id, client_name)
        if not client:
            #未注册
            return 20010#CLIENT_NOT_FIND
        client_state = client.get('state')
        if client_state == CLIENT_UNPASS:
            #未验证
            return 20001#CLIENT_UNPASS
        elif client_state == CLIENT_PASS:
            login_state =client.get("login")
            if login_state == CLIENT_LOGGING:
                #TODO:已登录的情况，重新登录? 单点登录?
                return 20013#CLIENT_LOGGING
            elif login_state == CLIENT_UNLOGGING:
                #未登录，登录
                self._login(client_id)
                return 20014#CLIENT_UNLOGGING
            else:
                logging.error("登录失败, client_id:%s, client_name:%s --> login_state:%s" % (client_id, client_name, login_state))
                return 1
        else:
            logging.error("登录失败, client_id:%s, client_name:%s --> client_state:%s" % (client_id, client_name, client_state))

    def get_client_id_by_name(self, client_name):
        client = self.get_client(client_name=client_name)
        client_id = client.get("id")
        if client_id:
            return client_id

    def get_client(self, client_id=-1, client_name=""):
        "检查客户端"
        if client_id > 0 and client_name:
            sql = "select * from %s where id=%s and name='%s'" % (self._table_name, client_id, client_name)
        elif client_id > 0:
            sql = "select * from %s where id=%s;" % (self._table_name, client_id)
        elif client_name:
            sql = "select * from %s where name='%s';" % (self._table_name, client_name)
        logging.info(sql)
        clients = self._mysql.select(sql)
        #clients = [{"id":1, "name":"zhipeng", "state":"0", "login":"0"}]
        return clients[0] if clients else {}

    def _login(self, client_id):
        sql = "UPDATE %s SET `login`=%d, `last_time`=now() WHERE `id`=%s;" % (self._table_name, CLIENT_LOGGING, client_id)
        return self._mysql.update(sql)


if __name__ == "__main__":
    pass
