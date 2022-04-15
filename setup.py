"""
@author: yudeqiang
@file: setup.py
@time: 2022/04/15
@describe: 
"""
# -*- coding: utf-8 -*-
from os.path import dirname, join
from sys import version_info

import setuptools

if version_info < (3, 6, 0):
    raise SystemExit("Sorry! feapder requires python 3.6.0 or later.")

with open(join(dirname(__file__), "plana/core/VERSION"), "rb") as f:
    version = f.read().decode("ascii").strip()

# with open("README.md", "r") as fh:
#     long_description = fh.read()

packages = setuptools.find_packages()

requires = [
    "redis==4.2.2",
    "pymongo==4.1.1",
    "APScheduler==3.8.1",
    "loguru==0.6.0",
    "better-exceptions>=0.2.2",
]
setuptools.setup(
    name="plana",
    version=version,
    author="yudeqiang",
    license="MIT",
    author_email="yudeqang@gmail.com",
    python_requires=">=3.6",
    description="plana是一个定时任务框架，包含任务运行信息，异常提醒等功能",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    install_requires=requires,
    url="https://github.com/yudeqang",
    packages=packages,
    include_package_data=True,
    classifiers=["Programming Language :: Python :: 3"],
)