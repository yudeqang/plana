"""
@author: yudeqiang
@file: cron.py
@time: 2022/04/13
@describe: 
"""
from plana.core import add_job, CronTrigger


@add_job(CronTrigger(second=3))
def say_hello_cron():
    """cron 示例"""
    print("hello world cron")
