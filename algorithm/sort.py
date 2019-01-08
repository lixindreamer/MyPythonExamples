# -*- coding: utf-8 -*-
"""
@author: lixin
@file: sort.py
@time: 2018/12/27 10:31
@software: PyCharm
@description: 经典的线性排序算法
"""
from typing import Sequence


def bubble_sort(a: Sequence[int]):
    """冒泡排序
    冒泡排序只会操作相邻的两个数据，每次冒泡操作都会对相邻的两个元素进行比较，看是否满足大小关系要求，
    如果不满足就互换。一次冒泡会至少让一个元素移动到它应该在的位置。
    时间复杂度为O(n**2)，最好情况下为O(n),需要1次冒泡,最坏的情况为O(n**2)，需要6次冒泡。
    空间复杂度为O(1)，是原地排序
    稳定排序：是

    :param a: 数组
    """
    list_len = len(a)
    for i in range(0, list_len):
        # 提前退出冒泡循环的标志位
        flag = False
        for j in range(0, list_len - i - 1):
            if a[j] > a[j + 1]:
                tmp = a[j]
                a[j] = a[j + 1]
                a[j + 1] = tmp
                flag = True

        # 没有数据交换，提前退出
        if not flag:
            break

def insert_sort(a: Sequence[int]):
    """插入排序
    将数组中的数据分为两个区间，已排序区间和未排序区间。初始已排序区间只有一个元素，
    就是数组的第一个元素。插入算法的核心思想是取未排序区间中的元素，在已排序区间找到合适的插入位置并将其插入，
    并保证已排序区间数据一直有序。重复这个过程，直到未排序区间中元素为空，算法结束。
    元素移动的次数。
    时间复杂度O(n**2),最好的情况下为O(n)即数组为正序排列，最坏的情况我O(n**2)即数组为逆序排列。
    空间复杂度O(1),是原地排序
    稳定排序：是
    :param a:
    :return:
    """
    list_len = len(a)

    if list_len <= 1:
        return

    for i in range(1,list_len):
        value = a[i]
        j = i - 1
        while j >= 0:
            if a[j] > value:
                # 数据异动
                a[j+1] = a[j]
                j -= 1
            else:
                break
        # 插入数据
        a[j+1] = value


if __name__ == '__main__':
    a = [2,4,1,9,23,12,8]
    # bubble_sort(a)

    insert_sort(a)

    print(a)
