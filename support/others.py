#! /usr/bin/env python3
# -*- coding:utf-8 -*-
import time

class TimeInfo():
    def get_localtime(self):
        localtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # 当前时间
        return localtime

class DealKey():
    def search_key(self,key): #根据关键词进行检索
        zh_model = re.compile(u'[\u4e00-\u9fa5]')
        match = zh_model.search(key)
        if match: #判断是否包含汉字，如果包含则对汉字做处理
            key = quote(key)
        return key


