"""
@author: yudeqiang
@file: test_backend.py
@time: 2022/04/18
@describe: 
"""
from plana.core import Job, SxBlockingScheduler, Task
from plana.core.backend import MemoryJobBackend, MemoryTaskBackend, MongoTaskBackend, MongoJobBackend


def test_memory():
    sc = SxBlockingScheduler(MemoryJobBackend())
    job = Job(sc, name='test')
    sc.register_job(job)
    print(sc.backend.get_all_job())
    assert len(sc.backend.get_all_job()) > 0

    t = MemoryTaskBackend()
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
    sc = SxBlockingScheduler(mb)
    job = Job(sc, name='test')
    sc.register_job(job)
    print(sc.backend.get_all_job())
    assert len(sc.backend.get_all_job()) > 0

    t = MongoTaskBackend('mongodb://192.168.0.132:27017')
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
