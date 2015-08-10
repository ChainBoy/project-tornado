# -*- coding:utf-8 -*-


# @version: 1.0
# @author: daichi
# @date: '14-8-8'


def read_lines(file_name):
    return_list = []
    file = open(file_name, 'r')
    lines = file.readlines()
    for line in lines:
        return_list.append(line.strip())
    file.close()
    return return_list

if __name__=='__main__':
    pass