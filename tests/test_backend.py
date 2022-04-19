"""
@author: yudeqiang
@file: test_backend.py
@time: 2022/04/18
@describe: 
"""
from apscheduler.triggers.cron import CronTrigger

from plana.core import Job, SxBlockingScheduler, Task, add_job
from plana.core.Exceptions import DuplicateJobId
from plana.core.backend import MemoryJobBackend, MemoryTaskBackend, MongoTaskBackend, MongoJobBackend


def test_memory():
    t = MemoryTaskBackend()
    sc = SxBlockingScheduler(MemoryJobBackend(), t)
    job = Job(sc, name='test')
    sc.register_job(job)
    print(sc.backend.get_all_job())
    assert len(sc.backend.get_all_job()) > 0

    task = Task(job, t)
    # 模拟任务启动
    task.start()
    ts = t.get_task(task.task_id)
    assert ts.get('start_time')
    # 任务结束
    task.stop()
    ts2 = t.get_task(task.task_id)

    assert ts2.get('end_time')


def test_mongo():
    mb = MongoJobBackend('mongodb://192.168.0.132:27017')
    t = MongoTaskBackend('mongodb://192.168.0.132:27017')
    sc = SxBlockingScheduler(mb, t)
    job = Job(sc, name='test')
    sc.register_job(job)
    print(sc.backend.get_all_job())
    assert len(sc.backend.get_all_job()) > 0

    task = Task(job, t)
    # 模拟任务启动
    task.start()
    ts = t.get_task(task.task_id)
    assert ts.get('start_time')
    # 任务结束
    task.stop()
    ts2 = t.get_task(task.task_id)

    assert ts2.get('end_time')

    # 清理掉测试集合
    mb.col.delete_many({})
    t.col.delete_many({})


def test_singletons():
    m = MemoryJobBackend()
    t = MemoryTaskBackend()
    s = SxBlockingScheduler(m, t)
    s1 = SxBlockingScheduler(m, t)
    assert s is s1


def test_dup():

    try:
        @add_job(CronTrigger(minute='20', hour='15', second='0'), name='测试notice')
        def test1():
            pass

        @add_job(CronTrigger(minute='20', hour='15', second='0'), name='测试notice')
        def test1():
            pass
    except DuplicateJobId:
        pass
