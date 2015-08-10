# -*- coding:utf-8 -*-


# @version: 1.0
# @author: Zhipeng Zhang
# @date: '2015/4/14'
from datetime import date
import simplejson


class DefaultJsonEncode(simplejson.JSONEncoder):
    def default(self, o):
        if isinstance(o, date):
            return o.__str__()


def dump(*args, **kwargs):
    kwargs['cls'] = DefaultJsonEncode
    return simplejson.dump(*args, **kwargs)


def dumps(*args, **kwargs):
    kwargs['cls'] = DefaultJsonEncode
    return simplejson.dumps(*args, **kwargs)


def load(*args, **kwargs):
    return simplejson.load(*args, **kwargs)


def loads(*args, **kwargs):
    return simplejson.loads(*args, **kwargs)


if __name__ == "__main__":
    from  datetime import datetime

    print dumps(date(2014, 1, 1))
    print dumps(datetime.now())
    print dumps(datetime(2015, 4, 8, 20, 22, 54))
