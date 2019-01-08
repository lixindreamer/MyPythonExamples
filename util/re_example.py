# -*- coding: utf-8 -*-
"""
@author: lixin
@file: re_example.py
@time: 2018/12/24 16:01
@software: PyCharm
@description: 使用正则表达式处理自定义的html标签。
"""
import re

s='''<lx_test>1234<lx_right type="company" attr2="123456">这是一段测试文本：<a href="https://baidu.comn">今天天气不错。</a></lx_right></lx_test>'''
s1='''<lx_right type="company" attr2="123456">这是一段测试文本：<lx_url type="xjbt" value="123456">今天天气不错。</lx_url></lx_right>'''
s2 = '''<lx_right type="company" attr2="123456">这是一段测试文本：<a href="https://baidu.comn">今天天气不错。</a></lx_right>'''
s3 = """<lx_test>1234</lx_test>"""

# 查询包含<lx_xxxx></lx_xxxx>但是同时内部不包含此类标签的字符
pattern = "<(?P<label>lx_[\w]+)[^<]*>(((?!<lx_).)+)</(?P=label)>"

# 查询包含<lx_xxxx></lx_xxxx>，同时标签内部仍然有<lx_xxx>标签的文本
pattern1 = "<(?P<label>lx_[\w]+)[^<]*>(.*?(<lx_).*?)</(?P=label)>"

# 包含HTML标签
pattern2 = "<[\s\S]+?>"

ret = re.search(pattern1,s)

# ret.group(2)即为匹配出来的结果值，再根据具体情况做进一步的过滤
# print(ret.groups())
# print(ret.group(2))


def find_lx_tag(txt):
    ret = re.search(pattern1,txt)
    # 把文本中的<lx_xxx>标签脱掉
    if ret is not None:
        return find_lx_tag(ret.group(2))
    else:
        ret_2 = re.search(pattern,txt)
        if ret_2 is not None and re.search(pattern2,ret_2.group(2)) is not None:
            return ret_2.group(2)
        else:
            return None


print(find_lx_tag(s))
print(find_lx_tag(s1))
print(find_lx_tag(s2))
print(find_lx_tag(s3))

if __name__ == '__main__':
    pass