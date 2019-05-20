#! /usr/bin/env python3
# -*- coding:utf-8 -*-
import os

from support.mysql import QccMysql as db

class ComBase():
    def set_method(self):
        mth1 = 0
        mth2 = 1
        return mth1,mth2

    def sql(self):
        ins = """
        SELECT * FROM `com_info` 
        WHERE 'kw' IS NOT NULL 
        AND 'com_id' IS NULL
        ORDER BY RAND() LIMIT 1;
        """
        return ins

    def get_com_li(self):
        com_file = os.path.abspath(os.path.join(os.getcwd(),'../../doc/company_list'))
        with open(com_file, 'r', encoding='utf-8') as rf:
            rf = rf.readlines()
        com_li = []
        for company in rf:
            company = company.strip()
            com_li.append(company)
        return com_li

    def get_com_name(self,sql):
        com_name = db().inssts(sql)
        return com_name



if __name__ == '__main__':
        com_li = ComBase().get_com_li()
        print(com_li)

