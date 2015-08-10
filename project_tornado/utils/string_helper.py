# -*- coding:utf8 -*-
#@date '2015-04-10'
#@author 'zhangzhipeng'


class StringHelper(object):
    def __init__(self):
        pass

    @staticmethod
    def s2i(text, default=0):
        if type(text) == int:
            return text
        text_int = default
        try:
            text_int = int(text)
        except ValueError:
            pass
        finally:
            return text_int

if __name__ == "__main__":
    print StringHelper.s2i("0")
    print StringHelper.s2i("10")
    print StringHelper.s2i(20)
    print StringHelper.s2i("")
    print StringHelper.s2i("", default=-1)
