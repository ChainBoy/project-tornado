# -*- coding:utf-8 -*-


# @version: 1.0
# @author: daichi
# @date: '15-5-28'
from project_tornado.utils.file_util import read_lines
from project_tornado.utils.singleton import singleton


@singleton
class WeatherCityManager():
    def __init__(self):
        self._CITY_FILE_NAME = "conf/wth_city"
        self.city_code_to_name = self._load_cities()

    def _load_cities(self):
        city_code_to_name = {}
        lines = read_lines(self._CITY_FILE_NAME)
        for line in lines:
            line = line.decode('utf8').strip()
            city_name, city_code = line.split('\t')
            city_code_to_name[city_code] = city_name
        return city_code_to_name

if __name__ == "__main__":
    pass
