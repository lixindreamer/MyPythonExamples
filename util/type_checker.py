# -*- coding: utf-8 -*-
"""
@author: lixin
@file: type_checker.py
@time: 2018/12/21 11:27
@software: PyCharm
@description: <module的描述信息>
"""
from typing import Tuple, Callable
from functools import wraps
import inspect
from collections import namedtuple, OrderedDict


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

        print("bound_types:", bound_types)

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


class Descriptor:
    def __init__(self, name=None, **opts):
        self.name = name
        for key, value in opts.items():
            setattr(self, key, value)

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value


def Typed(excepted_type, cls=None):
    """
    Decorator for applying type checking
    :param excepted_type:
    :param cls:
    :return:
    """
    if cls is None:
        return lambda cls: Typed(excepted_type, cls)
    super_set = cls.__set__

    def __set__(self, instance, value):
        if not isinstance(value, excepted_type):
            raise TypeError('expected' + str(excepted_type))
        super_set(self, instance, value)

    cls.__set__ = __set__

    return cls


def Unsigned(cls):
    """
    Decorator for unsigned value
    :param cls:
    :return:
    """
    super_set = cls.__set__

    def __set__(self, instance, value):
        if value < 0:
            raise ValueError("Expected >=0")
        super_set(self, instance, value)

    cls.__set__ = __set__

    return cls


def LimitSized(cls):
    """
    Decorator for allowing limit the size of values
    :param cls:
    :return:
    """
    super_init = cls.__init__

    def __init__(self, name=None, **opts):
        if 'upper' not in opts or 'lower' not in opts:
            raise TypeError('must provide upper and lower option')

        super_init(self, name, **opts)

    cls.__init__ = __init__

    super_set = cls.__set__

    def __set__(self, instance, value):
        if value > self.upper or value < self.lower:
            raise ValueError('value must be between {} and {}'.format(self.lower,self.upper))

        super_set(self, instance, value)

    cls.__set__ = __set__

    return cls


@Typed(int)
class Integer(Descriptor):
    pass

@LimitSized
class LimitedInteger(Integer):
    pass

@Unsigned
class UnsignedInteger(Integer):
    pass


@Typed(float)
class Float(Descriptor):
    pass


@Unsigned
class UnsignedFloat(Float):
    pass


@Typed(str)
class String(Descriptor):
    pass



if __name__ == '__main__':
    class A:
        a = String("a")
        b = UnsignedInteger("b")
        c = LimitedInteger("c",upper=10,lower=2)

        def __init__(self,a,b,c):
            self.a = a
            self.b = b
            self.c = c


    a1 = A("test",1,10)
    a2 = A("test",2,1)
    # a2 = A("test",-1,10)
