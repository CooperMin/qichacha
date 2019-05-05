#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import random
from support.cookies import Cookies as ck

class GeneralHeaders():
    def choice_ua(self):
        ua_dict = {
            'Firefox':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0',
            'Chrome':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36',
            'Safari':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1 Safari/605.1.15',
            'Edge':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763',
            'IE11':'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
        }
        ua_li = list(ua_dict.keys())
        name = random.choice(ua_li)  # 随机获取一条cookie值
        ua = ua_dict[name]
        return ua

    def header(self):
        header = {
            'Host': 'www.qichacha.com',
            'User-Agent': GeneralHeaders().choice_ua(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': 'keep-alive',
            'Cookie': ck().choice_cookie(),
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        }
        return header