"""
@author: yudeqiang
@file: __init__.py.py
@time: 2022/04/15
@describe: 
"""
import importlib
import importlib.util
from pathlib import Path
import os

from .core import *
from .settings import WORK_MODULE

MODULE_EXTENSIONS = '.py'


def package_contents(package_name):
    """查找模块下有哪些py文件"""
    spec = importlib.util.find_spec(package_name)
    if spec is None:
        return set()

    pathname = Path(spec.origin).parent
    ret = set()
    with os.scandir(pathname) as entries:
        for entry in entries:
            if entry.name.startswith('__'):
                continue
            current = '.'.join((package_name, entry.name.partition('.')[0]))
            if entry.is_file():
                if entry.name.endswith(MODULE_EXTENSIONS):
                    ret.add(current)
            elif entry.is_dir():
                ret.add(current)
                ret |= package_contents(current)

    return ret


content = package_contents(WORK_MODULE)
for c in content:
    importlib.import_module(c)

