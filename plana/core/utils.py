"""
@author: yudeqiang
@file: utils.py
@time: 2022/04/18
@describe: 
"""
import datetime
import hashlib

import pytz


def now() -> datetime.datetime:
    return datetime.datetime.now(pytz.timezone('Asia/Shanghai'))


def str_now() -> str:
    return now().strftime('%Y-%m-%d %H:%M:%S')


def hashify_str(s: str) -> str:
    sha = hashlib.sha1()
    sha.update(s.encode())
    return sha.hexdigest()
