# -*- coding: utf-8 -*-
"""
@author: lixin
@file: binary_search_tree.py
@time: 2018/12/27 10:11
@software: PyCharm
@description: 二分查找树
二分查找树，在树中的任意一个节点，其左子树中的每个节点的值，都要小于这个节点的值，
而右子树节点的值都大于这个节点的值。
"""
from queue import Queue


class TreeNode:
    def __init__(self, value: int):
        self.val = value
        self.left = None
        self.right = None
        self.parent = None

    def __str__(self):
        return "val:" + str(self.val)

    def __repr__(self):
        return self.__str__()


class BinarySearchTree:
    def __init__(self, val_list=None):
        self.root = None
        if val_list is not None:
            for n in val_list:
                self.insert(n)

    def insert(self, data):
        pass

    def _del(self,node: TreeNode):
        """从二叉树中删除数据
        所删除的节点N存在以下情况：
        1.没有子节点：直接删除N的父节点指针
        2.有一个子节点：将N父节点指针指向N的子节点
        3.有两个子节点：找到右子树的最小节点M，将值赋给N,然后删除M
        :param node:
        :return:
        """
        # 没有子节点：直接删除N的父节点指针
        if node.left is None and node.right is None:
            # 情况1和2，根节点和普通节点的处理方式不同
            if node == self.root:
                self.root = None
            else:
                if node.val < node.parent.val:
                    node.parent.left = None
                else:
                    node.parent.right = None

                node.parent = None

        # 有一个子节点：将N父节点指针指向N的子节点
        elif node.left is None and node.right is not None:
            if node == self.root:
                self.root = node.right
                node.right.parent = None
                node.right = None
            else:
                if node.val < node.parent.val:
                    node.parent.left = node.right
                else:
                    node.parent.right = node.right

                node.right.parent = node.parent
                node.parent = None
                node.right = None
        elif node.right is None and node.left is not None:
            if node == self.root:
                self.root = node.left
                node.left.parent = None
                node.left = None
            else:
                if node.val < node.parent.val:
                    node.parent.left = node.left
                else:
                    node.parent.right = node.left

                node.left.parent = node.parent
                node.parent = None
                node.left = None

        # 有两个子节点：找到右子树的最小节点M，将值赋给N,然后删除M
        else:
            min_node = node.right
            if min_node.left:
                min_node = min_node.left

            if node.val != min_node.val:
                node.val = min_node.val
                self._del(min_node)
            # 将所有重复的值都删除掉
            else:
                self._del(min_node)
                self._del(node)


def tree_deep(root: TreeNode) -> int:
    """
    求根节点的高度,起点高度为1。基于深度优先遍历，通过递归计算高度。max(左子树高度，右子树高度) + 1
    :param root:
    :return:
    """
    if root is None:
        return 0

    left = tree_deep(root.left)
    right = tree_deep(root.right)

    return left + 1 if left > right else right + 1


def reverse_tree(root: TreeNode) -> None:
    if root is None:
        return

    root.left, root.right = root.right, root.left
    reverse_tree(root.left)
    reverse_tree(root.right)


def in_order_traversal(root: TreeNode):
    """中序遍历
    中序遍历是指，对于树中的任意节点来说，先打印它的左子树，然后再打印它本身，
    最后打印它的右子树
    :param root:
    :return:
    """
    if root is None:
        return
    in_order_traversal(root.left)
    print(root)
    in_order_traversal(root.right)


def tree_width(root: TreeNode):
    """求树的宽度，通过层次遍历，计算每层的宽度，选择最大的宽度
    :param root:
    :return:
    """
    if root is None:
        return 0

    queue = Queue()
    max_width = 1
    curr_width = 1
    queue.put(root)
    while not queue.empty():
        while curr_width > 0:
            tmp = queue.get()
            if tmp.left is not None:
                queue.put(tmp.left)

            if tmp.right is not None:
                queue.put(tmp.right)

            curr_width -= 1
        curr_width = queue.qsize()
        max_width = max_width if max_width > curr_width else curr_width

    return max_width


def tree_deep2(root: TreeNode):
    """求根节点的高度,起点高度为1, 通过层次遍历，每经过一层深度加1

    :param root:
    :return:
    """
    if root is None:
        return 0

    queue = Queue()
    deep = 0
    curr_width = 1
    queue.put(root)

    while not queue.empty():
        while curr_width > 0:
            tmp = queue.get()
            if tmp.left is not None:
                queue.put(tmp.left)
            if tmp.right is not None:
                queue.put(tmp.right)

            curr_width -= 1
        curr_width = queue.qsize()
        deep += 1

    return deep


def rebuild_binary_tree():
    """重建二叉树
    https://mp.weixin.qq.com/s/ONKJyusGCIE2ctwT9uLv9g
    :return:
    """
    pass


if __name__ == '__main__':
    root_node = TreeNode(1)
    node_1_1 = TreeNode(2)
    root_node.left = node_1_1
    node_1_2 = TreeNode(3)
    root_node.right = node_1_2
    node_2_1 = TreeNode(4)
    node_2_2 = TreeNode(5)
    node_2_3 = TreeNode(6)
    node_2_4 = TreeNode(7)
    node_1_1.left = node_2_1
    node_1_1.right = node_2_2
    node_1_2.left = node_2_3
    node_1_2.right = node_2_4
    #
    # node_3_1 = TreeNode(8)
    # node_4_1 = TreeNode(9)
    # node_2_1.left = node_3_1
    # node_3_1.right = node_4_1

    print("tree deep:", tree_deep(root_node))
    print("tree deep2:", tree_deep2(root_node))
    # in_order_traversal(root_node)
    # reverse_tree(root_node)
    # in_order_traversal(root_node)
    print("tree width:", tree_width(root_node))
