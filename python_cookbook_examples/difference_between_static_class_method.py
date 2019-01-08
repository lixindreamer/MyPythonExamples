# -*- coding: utf-8 -*-
"""
@author: lixin
@file: difference_between_static_class_method.py
@time: 2018/12/21 10:49
@software: PyCharm
@description: <module的描述信息>
"""

class A:
    @staticmethod
    def func_static():
        pass

    @classmethod
    def func_class(cls):
        pass


if __name__ == '__main__':
    print(A.func_class)
    print(A.func_static)
    print(A.__dict__)
    a = A()
    print(a.func_class)
    print(a.func_static)
    print(a.__dict__)