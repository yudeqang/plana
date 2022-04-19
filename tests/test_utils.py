"""
@author: yudeqiang
@file: test_utils.py
@time: 2022/04/19
@describe: 
"""
from plana.core.utils import hashify_str


def test_hash():
    a = hashify_str('test')
    print(a)
