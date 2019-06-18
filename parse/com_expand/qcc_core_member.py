#! /usr/bin/env python3
# -*- coding:utf-8 -*-
"""
企查查-核心成员信息采集
"""
import time
import random
import requests

from support.others import TimeInfo as tm
from support.mysql import QccMysql as db
from support.headers import GeneralHeaders as gh
from parse.com_common.common import GeneralMethod as gm
class CoreMember():
    def __init__(self):
        self.gh = gh()
        self.db = db()
        self.gm = gm()
        self.tm = tm()
        self.index_url = 'https://www.qichacha.com'

    def get_com_id(self):
        cm = CoreMember()
        sel = """
        SELECT `com_id`,`com_name`,`status_`
        FROM `com_info`
        WHERE `chain` ='虚拟现实' 
        AND LENGTH(com_id) > 8 
        AND `area` = '山东省'
        AND `status_main_member` IS NULL
        ORDER BY RAND() LIMIT 1;
        """
        result = cm.db.selsts(sel)
        if result == ():
            result = [None, None, None]
        else:
            result = result[0]
        return result

    def get_column(self,sql): #接收sql语句，返回结果
        cm = CoreMember()
        result = cm.db.selsts(sql)[0]
        return result #返回元祖数据

    def verify_cond(self): #验证是否符合继续采集的条件
        cm = CoreMember()
        sel = """
        SELECT count(*) FROM `com_info`
        WHERE `chain` ='虚拟现实'
        AND LENGTH(com_id) > 8
        AND `area` = '山东省'
        AND `status_main_member` IS NULL;
        """
        result = cm.get_column(sel)[0]
        return result

    def count_sh_judge(self,com_id): #根据公司首页股东信息字段判断股东数量，模糊判断，需做二次判断
        cm = CoreMember()
        header = cm.gh.header()
        if com_id == None:
            count_cm = 0
        else:
            com_url = f'{sh.index_url}/firm_{com_id}.html'
            time.sleep(random.randint(3, 5))
            res = requests.get(com_url,headers=header).text
            tree = cm.gm.verify(res)
            try:
                count_cm = tree.xpath('//div[@class="company-nav-items"]/span[contains(text(),"核心人员")]/span/text()|//div[@class="company-nav-items"]/a[@data-pos="Mainmember"]/span/text()')[0]
                if count_cm == '999+':
                    count_cm = 999
                count_cm = int(count_cm)
            except:
                count_cm = 0
        status_column = 'status_main_member'
        count_column = 'count_main_member'
        gm().upd_status(com_id, status_column, count_column, count_sh)
        return count_cm

    def sh_page_judge(self,count_cm): #判断页码                                                           #判断是否是最近一或两年的招聘数据
        if count_cm == 0:
            cm_page_count = 0
        else:
            if count_cm % 10 == 0:
                cm_page_count = count_cm // 10
            else:
                cm_page_count = count_cm // 10 + 1
        return cm_page_count