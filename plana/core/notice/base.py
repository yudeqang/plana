"""
@author: yudeqiang
@file: base.py
@time: 2022/04/14
@describe: 
"""
from abc import ABC, abstractmethod


class Notice(ABC):

    @abstractmethod
    def notice(self, msg):
        pass
