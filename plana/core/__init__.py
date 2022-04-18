"""
@author: yudeqiang
@file: __init__.py
@time: 2022/04/13
@describe: 
"""
import functools
from typing import Optional

from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger

from .log import log
from .Exceptions import NoticeException
from .schedulers import MySchedulerBase, SxBlockingScheduler, SxBackgroundScheduler, Job
from ..settings import SCHEDULER_CLS, JOB_BACKEND_DB, TASK_BACKEND_DB
from .task import Task
from .backend import MongoJobBackend, MongoTaskBackend, MemoryTaskBackend, MemoryJobBackend
from .notice.base import Notice

if SCHEDULER_CLS == 'block':
    SCHEDULER_CLS = SxBlockingScheduler
elif SCHEDULER_CLS == 'background':
    SCHEDULER_CLS = SxBackgroundScheduler
else:
    print('未知的调度器')
    exit()

if JOB_BACKEND_DB == 'mongo':
    JOB_BACKEND_DB = MongoJobBackend
elif JOB_BACKEND_DB == 'memory':
    JOB_BACKEND_DB = MemoryJobBackend
else:
    print('未知的Job存储')
    exit()

if TASK_BACKEND_DB == 'mongo':
    TASK_BACKEND_DB = MongoTaskBackend
elif TASK_BACKEND_DB == 'memory':
    TASK_BACKEND_DB = MemoryTaskBackend
else:
    print('未知的任务存储')
    exit()


def schedulerFactory() -> MySchedulerBase:
    backend = JOB_BACKEND_DB()
    scheduler = SCHEDULER_CLS(backend, {
        # 'apscheduler.jobstores.default': {
        #     'type': 'redis',
        #     'host': '192.168.0.54',
        #     'password': '123456',
        #     'db': 1
        # },
        'apscheduler.executors.default': {
            'class': 'apscheduler.executors.pool:ThreadPoolExecutor',
            'max_workers': '20'
        },
        'apscheduler.job_defaults.coalesce': 'false',
        'apscheduler.job_defaults.max_instances': '3',
        'apscheduler.timezone': 'Asia/Shanghai',
    })
    return scheduler


scheduler = schedulerFactory()
task_backend_db = TASK_BACKEND_DB()


def add_job(trigger, name=None, notice: Optional[Notice] = None):
    """
    :param name: 为定时任务取一个名字，默认取函数的名字
    :param trigger: apscheduler.triggers.base.BaseTrigger trigger
    :param notice: 异常提醒 一个Notice实例
    :return:
    """

    def warp(func):
        nonlocal name
        if name is None:
            name = func.__name__

        @functools.wraps(func)
        @scheduler.scheduled_job(trigger, name=name)
        def inner(*args, **kwargs):
            job = scheduler.find_job(name)
            task = Task(job, task_backend_db)
            task.start()
            log.debug(f'{job.name}->开始执行')
            try:
                func(*args, **kwargs)
            except NoticeException as e:
                notice.notice(str(e))
                task.set_exception(e)
            except Exception as e:
                task.set_exception(e)
                log.error(f'{name}->执行异常:{str(e)}')
            finally:
                task.stop()
            log.debug(f'{name}->执行结束')

        return inner

    return warp


def start():
    scheduler.start()
