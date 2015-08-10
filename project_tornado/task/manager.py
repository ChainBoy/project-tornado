# -*- coding:utf-8 -*-


# @version: 1.0
# @author: Zhipeng Zhang
# @date: '2015/4/7'

import logging

from project_tornado.utils.compressor import Compressor
from project_tornado.utils.md5_checker import Md5Checker
from project_tornado.utils.mysql_helper import MysqlHelper


compressor = Compressor()
md5_checker = Md5Checker()


class Manager(object):
    def __init__(self, task_table="tasks", db_conf={}):
        self._task_table = task_table
        self._db_conf = db_conf
        self._mysql = MysqlHelper(**db_conf)

    def create(self):
        "创建任务"
        pass

    def cut(self):
        "切分任务"
        pass

    def update(self):
        "更新任务"
        pass

    def delete(self):
        "删除任务"
        pass

    def saver(self):
        "保存任务"
        pass
    #
    #def get_task(self, task_id, client_id, task_name):
    #    sql = "select 1 from tasks where task_id=%d and client_get_id=%d and task_name='%s';" % (task_id, client_id, task_name)

    def close(self, task_id, client_id):
        "完成某个任务，并且完成当前任务所对应的子任务、递归完成父任务."
        if self._close_children_task(task_id, client_id):
            return self._close_parent_task(task_id, client_id)
        return False

    def _close_parent_task(self, task_id, client_id):
        parent_task_id = self._find_parent_task_id(task_id)
        if parent_task_id == 0:
            return True
        sql = "select id from %s where parent_task_id = %d and c.state in (0, 1);" % (self._task_table, parent_task_id)
        logging.info(sql)
        # borther_tasks = [{"id":1}]
        borther_tasks = self._mysql.select(sql)
        if borther_tasks:
            #如果存在兄弟任务未完成，返回False
            return False
        else:
            #如果所有兄弟任务已完成，将父任务标记完成。递归父任务的兄弟任务。。
            self._done(parent_task_id, client_id)
            return self._close_parent_task(parent_task_id, client_id)

    def _close_children_task(self, task_id, client_id):
        sql = "select id from %s where parent_task_id = %d and state in (0, 1);" % (self._task_table, task_id)
        logging.info(sql)
        # child_tasks = [{"id": 1}, {"id":2}]
        child_tasks = self._mysql.select(sql)
        for child in child_tasks:
            if child.get("id"):
                return False
        self._done(task_id, client_id)
        return True

    def _find_parent_task_id(self, task_id):
        sql = "select parent_task_id as pid from %s where id=%d;" % (self._task_table, task_id)
        logging.info(sql)
        reset = self._mysql.select(sql)[0]
        return reset.get("pid")

    def _done(self, task_id, client_id):
        sql = "update %s set state = 10,end_client_id = %d where id = %d;" % (self._task_table, client_id, task_id)
        logging.info(sql)
        return self._mysql.update(sql)

    def get_md5(self, content, is_file=False):
        return md5_checker.md5(content)

    def un_compress(self, content, compress_type):
        return compressor.un_compress(content, compress_type=compress_type)

    def insert_data_row(self, sql):
        logging.info(sql)
        return self._mysql.insert(sql)

if __name__ == "__main__":
    pass
