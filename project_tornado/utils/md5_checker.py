# -*- coding:utf8 -*-

#@author: 'zhangzhipeng'
#@date: '2015-04-10'

import hashlib


class Md5Checker(object):
    def __init__(self):
        pass

    @staticmethod
    def str_2_md5(str):
        try:
            hash = hashlib.md5()
        except ImportError:
            # for Python << 2.5
            hash = hashlib.md5.new()
        hash.update(str)
        value = hash.hexdigest()
        return value

    def check(self, source, target):
        return get_md5(source) == get_md5(target)

    def md5(self, source, is_file=False):
        text = source
        if is_file:
            with file(source, "wb")as f:
                text = f.read()
        return hashlib.md5(text).hexdigest()

