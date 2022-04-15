"""
@author: yudeqiang
@file: backend.py
@time: 2022/04/15
@describe: 
"""
import datetime
from abc import ABC, abstractmethod

import pytz
from apscheduler.job import Job
from pymongo import MongoClient

from plana.settings import MONGO_URI


assert MONGO_URI


class JobBackendDb(ABC):

    @abstractmethod
    def register(self, job: Job):
        """注册一个Job到数据库中"""

    @abstractmethod
    def get_all_job(self) -> list:
        """获取所有的Job"""


class MongoJobBackend(JobBackendDb):

    def __init__(self):
        cli = MongoClient(MONGO_URI)
        db = cli['scheduler']
        self.col = db['job']

    def register(self, job: Job):
        if self.col.find_one({'job_id': job.id}):
            return
        self.col.insert_one({'job_id': job.id, 'job_name': job.name,
                             'registry_time': datetime.datetime.now(pytz.timezone('Asia/Shanghai'))})

    def get_all_job(self) -> list:
        return list(self.col.find({}, {'_id': 0}))


class TaskBackendDb(ABC):
    """Task的后端存储"""

    @abstractmethod
    def insert_task(self, task):
        pass

    @abstractmethod
    def update_task(self, condition, val):
        pass


class MongoTaskBackend(TaskBackendDb):

    def __init__(self):
        cli = MongoClient(MONGO_URI)
        db = cli['scheduler']
        self.col = db['task']

    def insert_task(self, data):
        self.col.insert_one(data)

    def update_task(self, condition, val):
        self.col.update_one(condition, val)

