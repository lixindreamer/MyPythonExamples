# -*- coding: utf-8 -*-
"""
@author: lixin
@file: decorator_examples.py
@time: 2018/12/20 12:40
@software: PyCharm
@description: python cookbook chapter 9
"""
from functools import wraps, partial
import logging

##  可自定义属性的装饰器 9.5##
def attach_wrapper(obj, func=None):
    if func is None:
        return partial(attach_wrapper, obj)
    setattr(obj, func.__name__, func)
    return func


def logged(level, name=None, message=None):
    """
    Add logging to a function
    :param level:
    :param name:
    :param message:
    :return:
    """

    def decorate(func):
        logname = name if name else func.__module__
        log = logging.getLogger(logname)
        logmsg = message if message else func.__name__

        @wraps(func)
        def wrapper(*args, **kwargs):
            log.log(level, logmsg)
            return func(*args, **kwargs)

        @attach_wrapper(wrapper)
        def set_level(newlevel):
            nonlocal level
            level = newlevel

        @attach_wrapper(wrapper)
        def set_message(newmsg):
            nonlocal logmsg
            logmsg = newmsg

        return wrapper

    return decorate


# Example use
@logged(logging.DEBUG)
def add(x, y):
    return x + y


@logged(logging.CRITICAL, 'example')
def spam():
    print("spam !")

##  可自定义属性的装饰器 ##


## 带可选参数的装饰器 9.6 ##

def logged_2(func=None,level=logging.DEBUG,name=None,message=None):
    if func is None:
        return partial(logged_2, level=level,name=name,message=message)

    logname = name if name else func.__module__
    log = logging.getLogger(logname)
    logmsg = message if message else func.__name__

    @wraps(func)
    def wrapper(*args,**kwargs):
        log.log(level,logmsg)
        return func(*args,**kwargs)

    return wrapper

@logged_2(level=logging.INFO)
def add_2(x,y):
    print("x+y=",str(x+y))

## 带可选参数的装饰器 9.6 ##

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    add.set_message("Add called")
    add.set_level(logging.ERROR)
    add(2, 3)
    spam()


    add_2(2,3)


