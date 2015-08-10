# -*- coding:utf-8 -*-


# @version: 1.0
# @author: Zhipeng Zhang
# @date: '2015/4/24'

class Enum():
    def __contains__(self, key):
        return True if key in dir(self) else False

def test():
    class ENUM_TASK_SAVE_TYPE(Enum):
        mysql = "mysql"
        file = "file"

    print "mysql" in ENUM_TASK_SAVE_TYPE.mysql
    # >>> True
    print "json" in ENUM_TASK_SAVE_TYPE.mysql
    # >>> False

if __name__ == "__main__":
    test()
