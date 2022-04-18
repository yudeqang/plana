"""
@author: yudeqiang
@file: test.py
@time: 2022/04/13
@describe: 
"""
from plana import start, content, add_job, NoticeException, IntervalTrigger, CronTrigger
from plana.core.notice.email import EmailNotice


notice = EmailNotice()


# @add_job(IntervalTrigger(seconds=10), name='测试notice', notice=notice)
@add_job(CronTrigger(minute='20', hour='15', second='0'), name='测试notice', notice=notice)
def test_notice():
    raise NoticeException('定时任务异常提醒测试, 这是为啥呢')


start()
