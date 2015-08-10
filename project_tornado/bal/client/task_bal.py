# -*- coding:utf-8 -*-


# @version: 1.0
# @author: Zhipeng Zhang
# @date: '2015/4/7'

import os
import re
import time
import stat
import logging
from project_tornado.model.task_entity import ENUM_TASK_SAVE_TYPE

from project_tornado.utils import json

from project_tornado.utils.compressor import Compressor, ENUM_SOURCE_TYPE
from project_tornado.utils.md5_checker import Md5Checker
from project_tornado.utils.mysql_helper import MysqlHelper


compressor = Compressor()
md5_checker = Md5Checker()


class TaskBal(object):
    def __init__(self, task_table="tasks", db_conf={}):
        self._task_table = task_table
        self._db_conf = db_conf
        self._mysql = MysqlHelper(**db_conf)

    def create(self, task):
        "创建任务, create_table_state 创建表状态, insert_task_state 插入任务列表状态"
        table_sql = task["table_sql"]
        create_table_state = self._create_table(table_sql)
        insert_task_state = 0
        if create_table_state:
            insert_task_state = self._insert_task(task)
        return create_table_state, insert_task_state

    def update_info(self, task):
        "更新任务状态信息"
        sql = "UPDATE " + self._task_table + "  SET `done_number`=%(done_number)s, `error_number`=%(error_number), `retry_number`=%(retry_number)s, `all_number`=%(all_number)s, `expect_end_time`=%(all_number)s WHERE  `id`=%(id);"
        return self._mysql.update(sql, task)

    def _create_table(self, sql):
        sql = re.sub(re.findall("create +table", sql, re.I)[0], "CREATE TABLE IF NOT EXISTS ", sql)
        create_result = self._mysql.insert(sql)
        if create_result >= 0:
            return 1
        else:
            return 0

    def _insert_task(self, task):
        sql = "INSERT INTO " + self._task_table + " (name, caption, start_cmd, config_path, files, create_user, client_create_id, state, parent_task_id, children_task_count, client_get_id, client_get_time,save_type, save_path, table_name, table_sql) VALUES (%(name)s, %(caption)s, %(start_cmd)s, %(config_path)s, %(files)s, %(create_user)s, %(client_create_id)s, %(state)s, %(parent_task_id)s, %(children_task_count)s, %(client_get_id)s, %(client_get_time)s, %(save_type)s, %(save_path)s, %(table_name)s, %(table_sql)s);"
        return self._mysql.insert(sql, task)

    def cut(self):
        "切分任务"
        pass


    def delete(self):
        "删除任务"
        pass

    def saver(self):
        "保存任务"
        pass

    def get_task(self, client_id, client_name, base_dir):
        """返回未完成任务列表、和新配发的任务。tuple([running_tasks], {new_task})
        如果不存在未完成的任务，返回空列表、并且配发空任务"""
        running_tasks = self._get_running_task(client_id, client_name)
        new_task = {}
        if not running_tasks:
            new_task = self._get_new_task()
            if new_task:
                task_id = new_task.get("id")
                # -------------------使用静态文件方式访问
                # files = [i.strip() for i in new_task.get("files").split("\n")]
                # new_task["files"] = files
                # -------------------使用静态文件方式访问
                # TODO: 此处提取file\config
                config_path = new_task.get("config_path")
                file_paths = new_task.get("files").split("\n")
                task_config = self._load_task_config(config_path, base_dir)
                task_files = self._load_task_files(file_paths, base_dir)
                new_task["config"] = task_config
                new_task["files"] = task_files
                # TODO: 此处提取file\config
                self._set_task_running(client_id, task_id)
        return running_tasks, new_task

    def _get_running_task(self, client_id, client_name):
        "获取客户端尚未完成的任务"
        sql = "select id, name, caption from %s where client_get_id=%s \
            and state=1 and create_user='%s';" % (self._task_table, client_id, client_name)
        logging.info(sql)
        tasks = self._mysql.select(sql)
        return tasks

    def _get_new_task(self):
        sql = "select id, name, start_cmd, caption, config_path, files, parent_task_id, children_task_count, save_type, save_path, table_name, table_sql from %s where state=0 and (children_task_count=0 or children_task_count=1) limit 1;" % self._task_table
        logging.info(sql)
        tasks = self._mysql.select(sql)
        return tasks[0] if tasks else {}

    def _set_task_running(self, client_id, task_id):
        sql = "UPDATE %s SET `state`=1, `client_get_id`=%s, `client_get_time`=NOW() WHERE `id`=%s;" % (
            self._task_table, client_id, task_id)
        logging.info(sql)
        return self._mysql.update(sql)

    def close(self, task_id, client_id):
        "完成某个任务，并且完成当前任务所对应的子任务、递归完成父任务."
        if self._close_children_task(task_id, client_id):
            return self._close_parent_task(task_id, client_id)
        return False

    def _load_task_config(self, config_path, base_dir):
        content = self.read_file(os.path.join(base_dir, config_path))
        config = {"path": config_path, "content": content}
        return config

    def _load_task_files(self, file_paths, base_dir):
        files = []
        for i in file_paths:
            content = self.read_file(os.path.join(base_dir, i))
            files.append({"path": i, "content": content})
        return files

    def read_file(self, file_path):
        content = ""
        with file(file_path)as f:
            content = f.read()
        return content

    def _close_parent_task(self, task_id, client_id):
        parent_task_id = self._find_parent_task_id(task_id)
        if parent_task_id == 0:
            return True
        sql = "select id from %s where parent_task_id = %d and c.state in (0, 1);" % (self._task_table, parent_task_id)
        logging.info(sql)
        # borther_tasks = [{"id":1}]
        borther_tasks = self._mysql.select(sql)
        if borther_tasks:
            # 如果存在兄弟任务未完成，返回False
            return False
        else:
            # 如果所有兄弟任务已完成，将父任务标记完成。递归父任务的兄弟任务。。
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

    def get_md5(self, content):
        return md5_checker.md5(content)

    def save_upload_data(self, save_type, file_name, file_content, base_dir, compress, delete_source=False, table_name=None):
        if save_type == ENUM_TASK_SAVE_TYPE.file:
            self.save_file(file_name, file_content, base_dir)
            return True, 0

        elif save_type == ENUM_TASK_SAVE_TYPE.mysql:
            self.un_compress(file_name, file_content, compress, base_dir, delete_source=True)
            source_file_name = file_name.rstrip(compress)[:-1]
            source_file_path = os.path.join(base_dir, source_file_name)
            if not os.path.isfile(source_file_path):
                return False, 0
            with file(source_file_path) as f:
                de_content = f.read()
                row = self._insert_content_to_db(table_name, de_content)
                os.remove(source_file_path)
                return True, row

    def save_file(self, file_name, content, base_dir=""):
        path = os.path.join(base_dir, file_name)
        dir_path = os.path.dirname(path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        with file(path, 'ab')as f:
            f.write(content)
        return True

    def un_compress(self, file_name, file_content, compress_type, base_dir, delete_source=False):
        file_path = os.path.join(base_dir, file_name)
        with file(file_path, "wb")as f:
            f.write(file_content)
        os.chmod(file_path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)
        compressor.un_compress(file_path, compress_type=compress_type, source_type=ENUM_SOURCE_TYPE.file,
                               save_dir=base_dir, delete_source=delete_source)

    def _insert_content_to_db(self, table_name, content):
        add_rows = 0
        for line_json in content.splitlines():
            line_dict = json.loads(line_json)
            sql = self._create_sql(table_name, line_dict)
            add_rows += self._insert_data_row(sql)
        return add_rows

    def _create_sql(self, table_name, data_dict):
        sql = "insert `%s`(%s) values('%s')" % (table_name, \
                                                     ", ".join(data_dict.keys()), \
                                                     "', '".join([i for i in data_dict.values()]))


    def _insert_data_row(self, sql):
        logging.info(sql)
        return self._mysql.insert(sql)


if __name__ == "__main__":
    pass
