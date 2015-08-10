# -*- coding:utf-8 -*-


# @version: 1.0
# @author: daichi
# @date: '15-5-28'

import redis
from project_tornado.utils.singleton import singleton

@singleton
class RedisClient():

    def __init__(self, host, port=6379):
        self._pool = redis.ConnectionPool(host=host, port=port, max_connections=100)


    def set(self, key, value, expire=None):
        r = redis.Redis(connection_pool=self._pool)
        r.set(key, value, expire)

    def set_batch(self, item_list):
        r = redis.Redis(connection_pool=self._pool)
        pipe = r.pipeline()
        for key, value, expire in item_list:
            pipe.set(key, value, expire)
        pipe.execute()

    def get_batch(self, key_list):
        data_map = {}
        r = redis.Redis(connection_pool=self._pool)
        for key in key_list:
            value = r.get(key)
            if value:
                data_map[key] = value
        return data_map

    def get(self, key):
        r = redis.Redis(connection_pool=self._pool)
        return r.get(key)

if __name__ == "__main__":
    redis_client = RedisClient('10.20.0.234')
    for i in range(10):
        key = 'DCS_dcs_new_pm25_石家庄'
        print(redis_client.get(key))
        print len(redis_client._pool._available_connections)
        print(len(redis_client._pool._in_use_connections))
