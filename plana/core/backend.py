"""
@author: yudeqiang
@file: backend.py
@time: 2022/04/15
@describe: 
"""
from abc import ABC, abstractmethod

from apscheduler.job import Job
from pymongo import MongoClient

from ..settings import MONGO_URI
from .utils import now, str_now


class JobBackendDb(ABC):

    @abstractmethod
    def register(self, job: Job):
        """注册一个Job到数据库中"""

    @abstractmethod
    def get_all_job(self) -> list:
        """获取所有的Job"""

    @property
    def now(self):
        return now()

    @property
    def str_now(self):
        return str_now()


class MongoJobBackend(JobBackendDb):

    def __init__(self, mongo_uri=None):
        if not mongo_uri:
            assert MONGO_URI
            mongo_uri = MONGO_URI
        cli = MongoClient(mongo_uri)
        db = cli['scheduler']
        self.col = db['job']

    def register(self, job: Job):
        if self.col.find_one({'job_id': job.id}):
            return
        self.col.insert_one({'job_id': job.id, 'job_name': job.name,
                             'registry_time': self.str_now})

    def get_all_job(self) -> list:
        return list(self.col.find({}, {'_id': 0}))


class MemoryJobBackend(JobBackendDb):

    def __init__(self):
        self.db = set()

    def register(self, job: Job):
        self.db.add(str({'job_id': job.id, 'job_name': job.name,
                         'registry_time': self.str_now}))

    def get_all_job(self) -> list:
        return [eval(i) for i in list(self.db)]


class TaskBackendDb(ABC):
    """Task的后端存储"""

    @abstractmethod
    def insert_task(self, task):
        pass

    @abstractmethod
    def get_task(self, task_id):
        pass

    @abstractmethod
    def update_task(self, old, new):
        """
        {'job_id': self.job.id, 'job_name': self.job.name,
        'task_id': self.task_id, 'start_time': self.now(),
        'end_time': self.end_time, 'run_time': self.run_time,
        'exception': self.exception}
        :param old: 旧的记录
        :param new: 新的数据
        :return:
        """
        pass


class MongoTaskBackend(TaskBackendDb):

    def __init__(self, mongo_uri=None):
        if not mongo_uri:
            assert MONGO_URI
            mongo_uri = MONGO_URI
        cli = MongoClient(mongo_uri)
        db = cli['scheduler']
        self.col = db['task']

    def insert_task(self, data):
        self.col.insert_one(data)

    def get_task(self, task_id):
        return self.col.find_one({'task_id': task_id}, {'_id': 0})

    def update_task(self, old, new):
        self.col.update_one({'task_id': old.get('task_id')}, {'$set': new})


class MemoryTaskBackend(TaskBackendDb):

    def __init__(self):
        self.db = list()

    def insert_task(self, task):
        self.db.append(task)

    def get_task(self, task_id):
        for i in self.db:
            if i.get('task_id') == task_id:
                return i

    def update_task(self, old, new):
        for ind, val in enumerate(self.db):
            if val.get('task_id') == old.get('task_id'):
                self.db[ind] = new
