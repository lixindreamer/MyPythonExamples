# -*- coding: utf-8 -*-
"""
@author: lixin
@file: tree_search.py
@time: 2018/12/27 9:26
@software: PyCharm
@description: 实现二叉树的遍历算法，基于递归算法
"""
from queue import Queue


class TreeNode:
    def __init__(self, value: int):
        self.val = value
        self.left = None
        self.right = None

    def __str__(self):
        return "val:" + str(self.val)

    def __repr__(self):
        return self.__str__()


# 层次遍历
def level_traversal(root: TreeNode):
    if root is None:
        return

    node_queue = Queue()
    node_queue.put(root)
    while not node_queue.empty():
        node = node_queue.get()
        print(node)
        if node.left is not None:
            node_queue.put(node.left)

        if node.right is not None:
            node_queue.put(node.right)


def pre_order_traversal(root: TreeNode):
    """前序遍历
    前序遍历是指，对于树中的任意节点来说，先打印这个节点，
    然后再打印它的左子树，最后打印它的右子树。
    :param root:
    :return:
    """
    if root is None:
        return
    print(root)
    pre_order_traversal(root.left)
    pre_order_traversal(root.right)

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

def post_order_traversal(root: TreeNode):
    """后序遍历
    后序遍历是指，对于树中的任意节点来说，先打印它的左子树，然后再打印它的右子树，
    最后打印这个节点本身。
    :param root:
    :return:
    """
    if root is None:
        return
    post_order_traversal(root.left)
    post_order_traversal(root.right)
    print(root)


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

    node_3_1 = TreeNode(8)
    node_2_1.left = node_3_1

    print("level traversal")
    level_traversal(root_node)

    print("pre-order traversal")
    pre_order_traversal(root_node)

    print("in-order traversal")
    in_order_traversal(root_node)

    print("post-order traversal")
    post_order_traversal(root_node)