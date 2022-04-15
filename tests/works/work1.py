"""
@author: yudeqiang
@file: work1.py
@time: 2022/04/13
@describe: 
"""
from plana.core import add_job, log, IntervalTrigger, scheduler, CronTrigger


@add_job(IntervalTrigger(seconds=2), '输出hello world')
def say_hello():
    """输出hello world"""
    log.info('hello world')


@add_job(CronTrigger(second=3))
def say_hello_cron():
    """cron 示例"""
    print("hello world cron")


if __name__ == '__main__':
    say_hello()
