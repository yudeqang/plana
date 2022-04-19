"""
@author: yudeqiang
@file: dingding.py
@time: 2022/04/15
@describe: 
"""
import json

import requests
from .base import Notice
from plana.settings import DING_TOKEN
from ..Exceptions import NotTokenException


class DingDingNotice(Notice):

    def __init__(self, token=None):
        if token:
            self.token = token
        else:
            if not DING_TOKEN:
                raise NotTokenException('钉钉token未提供')
            self.token = DING_TOKEN

    def notice(self, msg):
        url = f"https://oapi.dingtalk.com/robot/send?access_token={self.token}"
        data = {
            "msgtype": 'text',
            "text": {
                "content": msg
            }
        }
        json_data = json.dumps(data).encode(encoding='utf-8')
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
                   "Content-Type": "application/json"}
        return requests.post(url, data=json_data, headers=headers)
