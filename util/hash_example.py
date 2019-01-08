# -*- coding: utf-8 -*-
"""
@author: lixin
@file: hash_example.py
@time: 2018/12/26 18:18
@software: PyCharm
@description: 一致性哈希算法
"""
"""Consistent hashing is a special kind of hashing such that when a hash table is resized and consistent hashing is used,
 only K/n keys need to be remapped on average, where K is the number of keys, and n is the number of slots. In contrast, 
 in most traditional hash tables, a change in the number of array slots causes nearly all keys to be remapped."""
from hashlib import md5

# 所有机器列表
servers = [
    "192.168.1.1",
    "192.168.1.2",
    "192.168.1.3",
    # "192.168.1.4"
]

class HashRing(object):
    def __init__(self,nodes=None,replicas=3):
        """Manages a hash ring.

        `nodes` is a list of objects that have a proper __str__ representation.
        `replicas` indicates how many virtual points should be used pr. node,
        replicas are required to improve the distribution.
        :param nodes:
        :param replica:
        """
        self.replicas = replicas
        self.ring = dict()
        self._sorted_keys = []

        if nodes:
            for node in nodes:
                self.add_node(node)

    def add_node(self,node):
        """
        Adds a `node` to the hash ring (including a number of replicas).
        :param node:
        :return:
        """
        for i in range(0,self.replicas):
            key = self.gen_key('%s:%s' % (node,i))
            self.ring[key] = node
            self._sorted_keys.append(key)

        self._sorted_keys.sort()


    def remove_node(self,node):
        """
        Removes `node` from the hash ring and its replicas.
        :param node:
        :return:
        """
        for i in range(0,self.replicas):
            key = self.gen_key('%s:%s' % (node,i))
            del self.ring[key]
            self._sorted_keys.remove(key)

    def get_node(self,string_key):
        """
        Given a string key a corresponding node in the hash ring is returned.
        If the hash ring is empty, `None` is returned.
        :param string_key:
        :return:
        """
        return self.get_node_pos(string_key)[0]

    def get_node_pos(self,string_key):
        """
        Given a string key a corresponding node in the hash ring is returned
        along with it's position in the ring.
        If the hash ring is empty, (`None`, `None`) is returned.
        :param string_key:
        :return:
        """
        if not self.ring:
            return None,None

        key = self.gen_key(string_key)

        nodes = self._sorted_keys
        for i,node in enumerate(nodes):
            if key <= node:
                return self.ring[node],i
        return self.ring[nodes[0]], 0

    def gen_key(self,key):
        """
        Given a string key it returns a long value,
        this long value represents a place on the hash ring.
        md5 is currently used because it mixes well.
        :param key:
        :return:
        """
        m = md5()
        m.update(key.encode("utf-8"))
        return int(m.hexdigest(),16)

def consistent_hash():
    database = {}
    for s in servers:
        database[s] = []
    hr = HashRing(servers)

    for w in "abcdefghijklmn":
        database[hr.get_node(w)].append(w)

    print(database)


consistent_hash()


if __name__ == '__main__':
    pass
