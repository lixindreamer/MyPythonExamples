# -*- coding: utf-8 -*-
"""
@author: lixin
@file: tools.py
@time: 2018/12/20 11:24
@software: PyCharm
@description: 常用的工具方法
"""
import socket
import time
from typing import Tuple, Callable
from functools import wraps
import inspect
from collections import namedtuple, OrderedDict


def get_ip_host() -> Tuple[str, str]:
    """获取当前服务器的IP地址和主机名。
    :return: 服务器的IP地址和主机名
    """
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return ip, hostname


def current_time_millis() -> int:
    """获取当前的timestamp,以毫秒为单位，python的time.time()是以秒为单位的。Java 的System.milliseconds 是以毫秒为单位的。
    :return: 当前的timestamp
    """
    return int(time.time() * 1000)


def func_type_check(func: Callable) -> Callable:
    """Decorator, 用于校验函数的参数类型，参数类型需要在type hints中定义。
    :param func:
    :return:
    """
    msg = "Expected type {expected!r} for argument {argument},but got type {got!r} with value {value!r}"
    sig = inspect.signature(func)
    parameters = sig.parameters
    arg_keys = tuple(parameters.keys())

    @wraps(func)
    def wrapper(*args, **kwargs):
        CheckItem = namedtuple('CheckItem', ('annotation', 'argument_name', 'value'))
        check_list = []

        # collect args *args 传入的参数以及对应的函数参数注解
        for i, value in enumerate(args):
            argument_name = arg_keys[i]
            annotation = parameters[argument_name].annotation
            check_list.append(CheckItem(annotation, argument_name, value))

        # collect kwargs **kwargs 传入的参数以及对应的函数参数注解
        for arg_name, value in kwargs.items():
            annotation = parameters[arg_name].annotation
            check_list.append(CheckItem(annotation, arg_name, value))

        for item in check_list:
            if not isinstance(item.value, item.annotation) and item.annotation is not inspect.Signature.empty:
                error = msg.format(expected=item.annotation, argument=item.argument_name,
                                   got=type(item.value), value=item.value)
                raise TypeError(error)
        return func(*args, **kwargs)

    return wrapper


def func_type_assert(*ty_args, **ty_kwargs):
    """Decorator,通过在decorator中指定参数类型来限制强制函数的参数类型。
    :param ty_args: 参数类型
    :param ty_kwargs: 参数类型
    :return:
    """
    def decorator(func):
        # if in optimized mode, disable type checking
        if not __debug__:
            return func

        # Map function argument names to supplied types
        sig = inspect.signature(func)
        bound_types = sig.bind_partial(*ty_args, **ty_kwargs).arguments


        @wraps(func)
        def wrapper(*args, **kwargs):
            bound_values = sig.bind(*args, **kwargs)
            # Enforce type assertions across supplied arguments
            for name, value in bound_values.arguments.items():
                if name in bound_types:
                    if not isinstance(value, bound_types[name]):
                        raise TypeError('Argument {} must be {}.'.format(name, bound_types[name]))

            return func(*args, **kwargs)

        return wrapper

    return decorator


def timeit(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        start_time = time.time()
        ret = func(*args,**kwargs)
        print("duration:",time.time() - start_time)
        return ret
    return wrapper()


if __name__ == '__main__':
    import datetime


    @func_type_check
    def _test_func(a, b: datetime.datetime):
        pass


    _test_func(123, datetime.datetime.now())
    _test_func("weighted_round_robin", datetime.datetime.now())


    @func_type_assert(int,int)
    def _test_func2(a,b):
        pass

    _test_func2(1,2)
    _test_func2(1,"a")
