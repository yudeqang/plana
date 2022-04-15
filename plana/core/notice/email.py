"""
@author: yudeqiang
@file: email.py
@time: 2022/04/15
@describe: 
"""
from .base import Notice
import yagmail
from plana.settings import EMAIL_PWD, EMAIL_HOST, EMAIL_USER, EMAIL_TO_USER


class EmailNotice(Notice):

    def __init__(self, user=None, pwd=None, host=None, to_user=None):
        """
        :param user: 邮箱账户 e.g. ydq@qq.com
        :param pwd:  申请的IMAP密码
        :param host:  邮件服务器 e.g. smtp.qq.com
        :param to_user:  邮件接收人
        """
        if user:
            self.user = user
        else:
            assert EMAIL_USER
            self.user = EMAIL_USER

        if pwd:
            self.pwd = pwd
        else:
            assert EMAIL_PWD
            self.pwd = pwd

        if host:
            self.host = host
        else:
            assert EMAIL_HOST
            self.host = EMAIL_HOST

        if to_user:
            self.to_user = to_user
        else:
            assert EMAIL_TO_USER
            self.to_user = EMAIL_TO_USER

    def notice(self, msg):
        yag = yagmail.SMTP(user=EMAIL_USER, password=EMAIL_PWD, host=EMAIL_HOST)
        # 发送邮件
        title = '定时任务警告'
        yag.send(EMAIL_TO_USER, title, msg)
