#! /usr/bin/env python3
# -*- coding:utf-8 -*-
"""
企查查-信用信息
"""
import time
import random
import requests

from lxml import etree

from support.mysql import QccMysql as db
from support.others import TimeInfo as tm
from support.others import DealKey as dk
from support.headers import GeneralHeaders as gh

class Credit():
    def get_com_id(self):
        sel = """
        SELECT `com_id`,`com_name`
        FROM `com_info` 
        WHERE `origin` 
        IS NOT NULL AND LENGTH(`com_id`) > 5 AND `status_credit_execued` IS NULL
        ORDER BY RAND() LIMIT 1;
        """
        result = db().selsts(sel)
        if result == ():
            result = [None,None]
        else:
            result = result[0]
        return result

    def upd_status_execued(self,com_id,count):
        if count == -1:
            status = -1
        elif count == 0:
            status = 0
        else:
            status = 1
        upd = f"""
        UPDATE 
        `com_info` 
        SET
        `status_credit_execued` = "{status}",`count_credit_execued` = "{count}"
        WHERE 
        `com_id` = "{com_id}" ;
        """
        db().updsts(upd)

    def execued_judge(self):
        global com_id,com_name
        cd = Credit()
        count_execued = 0
        count = 0
        while count_execued == 0 or count_execued == -1:
            result = cd.get_com_id()
            com_id = result[0]
            com_name = result[1]
            if com_id == None:
                pass
            else:
                count += 1
                com_url = f'https://www.qichacha.com/firm_{com_id}.html'
                hds = gh().header()
                time.sleep(random.randint(2,4))
                res = requests.get(com_url, headers=hds).text
                tree = etree.HTML(res)
                # print(res)
                # print(com_url)
                try:
                    count_execued = tree.xpath(f'//div[@class="company-nav-items"]/span[contains(text(),"被执行人")]/span/text()|//div[@class="company-nav-items"]/a[@data-pos="zhixinglist"]/span/text()')[0]
                    count_execued = int(count_execued)
                except:
                    count_execued = -1
                localtime = tm().get_localtime()  # 当前时间
                print(localtime)
                print(count,com_id,count_execued)
                cd.upd_status_execued(com_id,count_execued)
        return com_id,com_name,count_execued

    def get_page_count(self):
        cd = Credit()
        result = cd.execued_judge()
        com_id = result[0]
        com_name = result[1]
        count_record = result[2]
        if count_record % 10 == 0:
            count_page = count_record // 10
        else:
            count_page = count_record // 10 + 1
        value = [com_id,com_name,count_page,count_record]
        return value

    def get_page_info(self):
        cd = Credit()
        value = cd.get_page_count()
        com_id = value[0]
        com_name = value[1]
        count_page = value[2]
        count_record = value[3]
        key = dk().search_key(com_name)

        f'https://www.qichacha.com/company_getinfos?unique={com_id}&companyname={com_name}&p={}&tab=susong&box=zhixing'













if __name__ == '__main__':
    cd = Credit()
    cd.execued_judge()

