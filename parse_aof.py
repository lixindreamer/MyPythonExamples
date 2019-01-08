# -*- coding: utf-8 -*-
"""
@author: lixin
@file: test_parse_aof.py
@time: 2019/1/8 14:07
@software: PyCharm
@description: <module的描述信息>
"""
from __future__ import print_function
import hiredis
import sys

if len(sys.argv) != 2:
    print("请提供aof文件路径！")
    sys.exit()
try:
    file = open(sys.argv[1],'rb')
    file.readlines()
    cur_request = b''
    while True:
        new = file.readline()
        cur_request = cur_request + new
        # Once all lines are read this just returns ''
        # until the file changes and a new line appears
        if new:
            req_reader = hiredis.Reader()
            # req_reader.setmaxbuf(0)
            req_reader.feed(cur_request)
            command = req_reader.gets()
            try:
                if command is not False:
                    print(command)
                    cur_request = b''
            except hiredis.ProtocolError:
                print("protocal error")

except (KeyboardInterrupt, SystemExit):
    file.close()


if __name__ == '__main__':
    pass