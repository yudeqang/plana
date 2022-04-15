## 简介
plana是一个非常简单的定时任务框架，内置了异常提醒和任务记录功能 \
现阶段使用需要配置一个MongoDB，因为还没有前端的展示功能，待后续开发，两天前萌生了一个想法，想要做一个定时任务框架，现在我的定时任务都基于linux的Crontab来管理，
许多小脚本存放于服务器的各个地方，想使用一种统一的方式来管理他们。开源的方案也有，看了一些任务调度框架，但是它们部署都挺麻烦，而且不一定适用，于是就有了这个项目，它是基于APScheduler开发的。

## 快速上手
```python
from plana.core import add_job, IntervalTrigger, start
from plana.core.notice import EmailNotice

# 使用EMAIL提醒需要提供settings.py配置文件或者实例化的时候传入参数
notice = EmailNotice()

@add_job(IntervalTrigger(seconds=3), name='你好啊', notice=notice)
def say_hello():
    """Interval 示例"""
    print("hello world")

start()
```
plana中有几个基本的对象
trigger 定时器，有两种选择，间隔时间，或者linux cron 格式的定时器，示例中使用的是间隔时间，每隔3秒运行一次
notice 提醒器，内置了两种，钉钉和邮件提醒
使用plana添加定时任务分为如下几步
1. 引入相关的对象
2. 使用add_job注册一个定时任务，需要提供trigger，name和notice是可选的，当你的任务需要异常提醒的时候要提供notice，建议提供name，这样有利于阅读
3. 编写定时函数内容
4. 运行start方法

## 触发异常提醒
要触发提醒，需要抛出一个NoticeException
```python
from plana.core.Exceptions import NoticeException

def test():
    raise NoticeException('定时任务异常啦')
```

![](./static/emailnotice.jpg)

## 配置文件
由于定时任务存储目前依赖于MongoDB，所有需要用户提供一个mongodb的连接
可选的配置：
```python
# Mongo连接， mongodb://root:123456@127.0.0.1:27017
MONGO_URI = ''

# 如果定时任务存在某个模块下，提供模块的名字
WORK_MODULE = 'work'

# 钉钉的Token
DING_TOKEN = ''

# 邮件设置
EMAIL_USER = ''  # 账户
EMAIL_PWD = ''  # IMAP密码
EMAIL_HOST = ''
EMAIL_TO_USER = ''
```

## todo
目前这个项目处于非常早期的版本，不足之处还有很多，后续要陆续优化 \
后续还打算提供一个简单的前端页面来展示定时任务运行记录 \
除了用MongoDB做任务存储以外，还要支持其他的数据库 \
为了再降低使用成本，还要添加基于内存的存储 
