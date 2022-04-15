"""
@author: yudeqiang
@file: interval.py
@time: 2022/04/13
@describe: 
"""
from plana.core import add_job, IntervalTrigger


@add_job(IntervalTrigger(seconds=3))
def say_hello():
    """Interval 示例"""
    print("hello world")
