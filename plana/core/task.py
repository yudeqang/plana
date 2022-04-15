"""
@author: yudeqiang
@file: task.py
@time: 2022/04/15
@describe: 
"""
import datetime
import uuid

import pytz

from .schedulers import Job
from .backend import TaskBackendDb


class Task:

    def __init__(self, job: Job, backend: TaskBackendDb):
        self.job = job
        self.backend = backend
        self.start_time = None
        self.end_time = None
        self.running = False
        self.run_time = None
        self.exception = None
        self.task_id = uuid.uuid4().hex

    def start(self):
        self.running = True
        self.start_time = self.now()
        self.backend.insert_task({'job_id': self.job.id, 'job_name': self.job.name,
                                  'task_id': self.task_id, 'start_time': self.now()})

    def stop(self):
        self.running = False
        self.end_time = self.now()
        self.run_time = str(self.end_time - self.start_time)  # 用字符串表示运行时间
        self.backend.update_task({'task_id': self.task_id}, {'$set': {'end_timd': self.end_time,
                                                                      'run_time': self.run_time,
                                                                      'exception': str(self.exception)}})

    @staticmethod
    def now() -> datetime.datetime:
        tz = pytz.timezone('Asia/Shanghai')
        return datetime.datetime.now(tz)

    def get_stats(self):
        return self.__str__()

    def __str__(self):
        name = self.job.name
        stats = '运行中' if self.running else '运行结束'
        return f"{name}->{stats}"

    def set_exception(self, exception: Exception):
        self.exception = exception

