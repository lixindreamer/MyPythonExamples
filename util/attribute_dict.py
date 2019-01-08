# -*- coding: utf-8 -*-
"""
@author: lixin
@file: attribute_dict.py
@time: 2018/12/28 10:19
@software: PyCharm
@description: 将dict转化为一个对象，可以像访问对象属性一样访问dict的key,例如a.b.c 等同于 a["b"]["c"]
"""
import copy
import pprint
import collections


class AttributeDict(object):
    """
       使dict的key值可以像对象的属性一样访问
    """

    def __init__(self, dict_object=None):
        """
        :param d: dict
        """
        self.__dict__ = copy.deepcopy(dict_object) if dict_object is not None else dict()
        for k, v in self.__dict__.items():
            if isinstance(v, dict):
                self.__dict__[k] = AttributeDict(v)

    def __repr__(self):
        return pprint.pformat(self.__dict__)

    def __iter__(self):
        return self.__dict__.__iter__()

    def update(self, other):
        AttributeDict._update_dict_recursive(self, other)

    def items(self):
        return self.__dict__.items()

    def keys(self):
        return self.__dict__.keys()

    def get(self, key, default_value=None):
        return self.__dict__.get(key, default_value)

    @staticmethod
    def _update_dict_recursive(target, other):
        if isinstance(other, AttributeDict):
            other = other.__dict__
        if isinstance(target, AttributeDict):
            target = target.__dict__

        for k, v in other.items():
            if isinstance(v, collections.Mapping):
                r = AttributeDict._update_dict_recursive(target.get(k, {}), v)
                target[k] = r
            else:
                target[k] = other[k]
        return target

    def convert_to_dict(self):
        result_dict = {}
        for k, v in self.__dict__.items():
            if isinstance(v, AttributeDict):
                v = v.convert_to_dict()
            result_dict[k] = v
        return result_dict


if __name__ == '__main__':
    a = {"k1":{"k2":{"k3":"abc"},"k4":123},"k5":2}
    attribute_dict = AttributeDict(a)
    print(attribute_dict.k1.k2.k3)
    attribute_dict.k1.k2.k3 = "efg"
    print(attribute_dict.k1.k2.k3)
    print(a)