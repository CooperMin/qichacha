#! /usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import requests

from urllib.parse import quote,unquote

from support.others import DealKey as dk
from support.headers import GeneralHeaders as gh


class Jarvis: #Jarvis-托尼的管家
    def __init__(self):
        self.index_url = 'https://www.qichacha.com/'
        self.gh = gh()
        self.dk = dk()

    def read_keywords(self):
        kwfile = os.path.abspath('../../doc/keywords')
        with open(kwfile,'r') as f:
            kw_li = f.readlines()
        new_kw_li = []
        for kw in kw_li:
            kw = kw.strip()
            new_kw_li.append(kw)
        return new_kw_li

    def search_key(self):
        jrs = Jarvis()
        kw_li = jrs.read_keywords()
        for key in kw_li:
            quote_key = jrs.dk.search_key(key)
            search_url = ''.join((jrs.index_url,'search?key=',quote_key))
            header = jrs.gh.header()
            header.update({'Referer':f'{search_url}'})
            print(header)
            res = requests.get(search_url,headers=header).text
            print(res)
            input('Pause')



if __name__ == '__main__':
    jrs = Jarvis()
    # Jarvis().read_keywords()
    jrs.search_key()
