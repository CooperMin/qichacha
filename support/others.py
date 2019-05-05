#! /usr/bin/env python3
# -*- coding:utf-8 -*-
import time

class timeInfo():
    def get_localtime(self):
        localtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # 当前时间
        return localtime