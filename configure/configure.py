# -*- coding:utf-8 -*-

# @version: 1.0
# @author: Zhipeng Zhang
# @date: '2015-04-07'
import os
import logging
import ConfigParser

# from configure.task_configure import TaskConfigure
import xmltodict


class Configure(object):
    def __init__(self, config_path=""):
        """
        加载xml配置文件.
        :param config_path:
        :return:
        """
        self._parser = None
        self._config = {}
        if not config_path:
            config_path = os.path.join(os.getcwd(), 'conf', \
                                       os.path.relpath(os.getcwdu(), '..') + '.xml')
        if config_path and os.path.exists(config_path):
            self._load_config(config_path)
        else:
            logging.error(u"未找到配置文件：%s，终止运行。" % config_path)
            exit(-9)

    def get_application_setting(self):
        config = self.get_config_setting("application")
        config['template_path'] = os.path.join(os.getcwdu(), config.get("base_dir", ""),
                                               config.get('template_path', 'template'))
        config['static_path'] = os.path.join(os.getcwdu(), config.get("base_dir", ""),
                                             config.get('static_path', 'static'))
        config['files_dir'] = os.path.join(config['static_path'], config.get("files_dir"))
        config['source_dir'] = os.path.join(config['static_path'], config.get("source_dir"))
        debug = config.get('debug', 'False')
        gzip = config.get('gzip', 'False')
        config['debug'] = True if debug.lower() == 'true' else False
        config['gzip'] = True if gzip.lower() == 'true' else False

        return config

    def get_database_setting(self):
        config = self.get_config_setting("database")
        config["pool_size"] = int(config.get("pool_size", 10))
        config["pool_name"] = config.get("port", "project_tornado_pool").replace(" ", "")
        config["port"] = int(config.get("port", 3306))
        config["commit_size"] = int(config.get("commit_size", 1000))
        return config

    def get_database_name(self):
        return self.get_database_setting().get("db")

    def get_redis_server(self):
        return self.get_config_setting("redis").get("server")

    def get_redis_port(self):
        return int(self.get_config_setting("redis").get("port"))

    def _load_config(self, config_path=""):
        # self._parser = ConfigParser.ConfigParser()
        #self._configureFileName = config_path
        config_xml = ""
        with file(config_path, 'r')as f:
            config_xml = f.read()
        if config_xml:
            self._config = xmltodict.parse(config_xml, encoding='utf8').get('project_tornado')
            #self._parser.readfp(f)

    def get_config_setting(self, config_key):
        """
        获取配置. 转化为标准字典。
        :return:
        """
        return self._ordered_dict_to_dict(self._config.get(config_key))

    def _ordered_dict_to_dict(self, ordered):
        result = {}
        for i in ordered:
            if i:
                result[i[1:]] = ordered[i]
        return result


    def _split_strip(self, string, split_char=",", remove_none=False):
        self._pass()
        if remove_none:
            return [i.strip() for i in string.split(split_char) if i.strip()]
        return [i.strip() for i in string.split(split_char)]

    def _pass(self):
        pass

    def _get_filed(self, section, option, parser=None, default="", json=False):
        if parser is None:
            if self._parser is not None:
                parser = self._parser
        if parser is None:
            logging.error(u"配置文件加载异常?parser is None. 请确认!")
            exit(-9)
        value = default
        try:
            value = parser.get(section, option).strip()
        except ConfigParser.NoOptionError, e:
            logging.info(u'节点:%s 没有配置子项:%s，E:%s' % (section, option, e))
        except ConfigParser.InterpolationMissingOptionError, e:
            value = e.message.split("rawval : ")
            if value and len(value) > 1:
                value = value[1]
            else:
                raise ConfigParser.Error
        if json:
            try:
                # value = sjson.loads(value)
                value = eval(value)
            except Exception, e:
                logging.error(u"配置文件值转化list发生异常，请确认。section:[%s], option:%s, value=%s." % (
                    section, option, value))
                exit(-9)
        return value

    def _get_keys(self, section, parser=None):
        keys = []
        if parser is None:
            if self._parser is not None:
                parser = self._parser
        if parser is None:
            logging.error(u"配置文件加载异常?parser is None. 请确认!")
            exit(-9)
        try:
            keys = parser.options(section)
        except ConfigParser.NoSectionError, e:
            logging.info(u'配置没有节点%s, E:%s' % (section, e))
        return keys


configure = Configure()

if __name__ == "__main__":
    pass
