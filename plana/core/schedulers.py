"""
@author: yudeqiang
@file: schedulers.py
@time: 2022/04/14
@describe: 
"""
from abc import ABC
from typing import List


from apscheduler.schedulers.base import BaseScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.job import Job
from apscheduler.util import _Undefined

from .backend import JobBackendDb, TaskBackendDb, MemoryTaskBackend, MemoryJobBackend

undefined = _Undefined()


class MySchedulerBase(BaseScheduler, ABC):

    _jobs: List[Job] = []

    _instance = None

    def __init__(self, backend: JobBackendDb,
                 task_backend: TaskBackendDb,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.backend = backend
        self.task_backend = task_backend

    def register_job(self, job):
        self._jobs.append(job)
        self.backend.register(job)

    def add_job(self, func, trigger=None, args=None, kwargs=None, id=None, name=None,
                misfire_grace_time=undefined, coalesce=undefined, max_instances=undefined,
                next_run_time=undefined, jobstore='default', executor='default',
                replace_existing=False, **trigger_args):
        job = super(MySchedulerBase, self).add_job(func, trigger, args, kwargs, id, name,
                                                   misfire_grace_time, coalesce, max_instances,
                                                   next_run_time, jobstore, executor,
                                                   replace_existing, **trigger_args)
        self.register_job(job)
        return job

    def find_job(self, name):
        for i in self._jobs:
            if i.name == name:
                return i
        raise Exception('job is not found')

    def __new__(cls, *args, **kwargs):
        if cls._instance:
            return cls._instance
        cls._instance = super(MySchedulerBase, cls).__new__(cls)
        return cls._instance


class SxBlockingScheduler(MySchedulerBase, BlockingScheduler):
    """
    阻塞的调度器，当程序中只有一个线程时使用
    """
    pass


class SxBackgroundScheduler(MySchedulerBase, BackgroundScheduler):
    """
    非阻塞的调度器，用在多线程任务中
    """
    pass
