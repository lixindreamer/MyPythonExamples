# -*- coding: utf-8 -*-
"""
@author: lixin
@file: decorator_examples2.py.py
@time: 2018/12/21 9:56
@software: PyCharm
@description: <module的描述信息>
"""

###  将装饰器定义为类的一部分 ###
from functools import wraps

class A:
    # Decorator as an instance method
    def decorator1(self,func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            print('Decorator 1')
            return func(*args,**kwargs)
        return wrapper

    # Decorator as a class method
    @classmethod
    def decorator2(cls,func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            print('Decorator 2')
            return func(*args,**kwargs)

        return wrapper

###  将装饰器定义为类的一部分 ###


### 创建一个动态计算的属性 ###
import datetime
class B:
    def get_current_time(self):
        return datetime.datetime.now()

    current_time = property(get_current_time)

### 创建一个动态计算的属性 ###


if __name__ == '__main__':
    a = A()
    @a.decorator1
    def spam():
        pass

    @A.decorator2
    def grok():
        pass

    import time

    b = B()

    print(b.current_time)
    time.sleep(2)
    print(b.current_time)