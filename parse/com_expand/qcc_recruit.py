#! /usr/bin/env python3
# -*- coding:utf-8 -*-
"""
企查查-招聘 信息采集
"""
import time
import random
import requests

from lxml import etree

from support.others import DealKey as dk
from support.mysql import QccMysql as db
from support.others import TimeInfo as tm
from support.headers import GeneralHeaders as gh
from parse.com_common.common import GeneralMethod as gm

class RecruitInfo():
    def __init__(self):
        self.rc = RecruitInfo()
        self.db = db()
        self.gh = gh()
        self.gm = gm()
        self.index_url = 'https://www.qichacha.com'

    def sql(self): #输出需要的sql查询结果
        sel = """
        SELECT com_id,com_name FROM `com_info` 
        WHERE origin IS NOT NULL 
        AND status_recruit IS NULL
        AND LENGTH(com_id) > 5
        ORDER BY RAND() LIMIT 1;
        """
        return sel

    def get_column(self,sql):
        result = db.selsts(sql)[0]
        return result

    def count_rc_judge(self,com_id): #根据公司首页招聘字段判断招聘数量，模糊判断，需做二次判断
        global count_rc
        if com_id == None:
            count_rc = 0
        else:
            count += 1
            com_url = f'https://www.qichacha.com/firm_{com_id}.html'
            hds = gh().header()
            time.sleep(random.randint(3, 5))
            res = requests.get(com_url, headers=hds).text
            tree = gm.verify(res)
            try:
                count_rc = tree.xpath('//div[@class="company-nav-items"]/span[contains(text(),"招聘")]/span/text()|//div[@class="company-nav-items"]/a[@data-pos="joblist"]/span/text()')[0]
                if count_rc == '999+':
                    count_rc = 999
                count_rc = int(count_rc)
            except:
                count_rc = 0
        return count_rc

    def get_count_rc(self,count_rc,key,count): #根据模糊判断，到招聘详情页判断出精确的招聘数量
        global res
        if count_rc > 0:
            info_url = f'https://www.qichacha.com/company_getinfos?unique={com_id}&companyname={key}&tab=run'
            hds = gh().header()
            time.sleep(random.randint(3, 5))
            res = requests.get(info_url, headers=hds).text
            tree = gm.verify(res)
            count_rc = tree.xpath('//a[contains(@onclick,"#joblist")]/text()')[0].split('招聘')[1].strip()
            count_rc = int(count_rc)
            localtime = tm().get_localtime()  # 当前时间
            print(localtime)
            print(f'计数器：{count}\n公司ID:{com_id}\n招聘岗位数：{count_rc}')
        status_column = 'status_recruit'  # 表字段名
        count_column = 'count_recruit'  # 表字段名
        gm.upd_status(com_id, status_column, count_column, count_rc)
        return count_rc,res

    def rc_judge(self): #返回精确的招聘数
        global com_id,com_name,res
        count_rc = 0
        count = 0
        while count_rc == 0:
            count += 1
            sql = self.rc.sql()
            result = self.rc.get_column(sql)
            com_id = result[0]
            com_name = result[1]
            key = dk().search_key(com_name)
            count_rc = self.rc.count_rc_judge(com_id)
            info = self.rc.get_count_rc(count_rc,key,count)
            count_rc = info[0]
            res = info[1]
        real_count_rc = count_rc
        result = [real_count_rc,com_id,com_name,res]
        return result

    def rc_page_judge(self): #判断页码                                                           #判断是否是最近一或两年的招聘数据
        result = self.rc.rc_judge()
        real_count_rc = result[0]
        com_id = result[1]
        com_name = result[2]
        res = result[3]
        if real_count_rc % 10 == 0:
            rc_page_count = real_count_rc // 10
        else:
            rc_page_count = real_count_rc // 10 + 1
        return rc_page_count,com_id,com_name,res

    def rc_detail_para(self,com_id,com_name,page):
        para = {
            'unique': f'{com_id}',
            'companyname': f'{com_name}',
            'p': page,
            'tab': 'run',
            'box': 'job'
        }
        return para

    def one_year_judge(self,date):
        a = [0,1]
        date_today_stamp = round(time.time())
        if type(date) == type(a):
            value = []
            for dt in date:
                date_stamp = round(time.strptime(dt,'%Y-%m-%d'))
                et = int((date_today_stamp - date_stamp) // 60*60*24*366)  # 计算时间差,天
                if et < 0:
                    et = -1
                value.append(et)
            if -1 in value:
                return False
            else:
                return True
        else:
            et = int((date_today_stamp - date_stamp) // 60 * 60 * 24 * 366)  # 计算时间差,天
            if et < 0:
                return False
            else:
                return True
    def get_info(self,rc_info_li,com_id,count):
        for nbr, info in enumerate(rc_info_li, 1):
            count += 1
            job_id = info.xpath('td[3]/a/@href')[0].split('jobdetail_')[1]
            rc_num = info.xpath('td[1]/text()')[0]
            pub_date = info.xpath('td[2]/text()')[0]
            rc_job = info.xpath('td[3]/a/text()')[0]
            salary = info.xpath('td[4]/text()')[0]
            education = info.xpath('td[5]/text()')[0]
            we = info.xpath('td[6]/text()')[0]
            city = info.xpath('td[7]/text()')[0]
            ins = f"""
            insert into table 
            (com_id,job_id,rc_num,pub_date,rc_job,salary,education,we,city)
            values 
            ("{com_id}","{job_id}","{rc_num}","{pub_date}","{rc_job}","{salary}","{education}","{we}","{city}");
            """
            self.db.inssts(ins)


    def rc_info(self):
        result = self.rc.rc_page_judge()
        rc_page_count = result[0]
        com_id = result[1]
        com_name = result[2]
        res = result[3]
        value = True
        count = 0
        while value == True:
            for page in range(1,rc_page_count+1):
                count += 1
                url = f'{self.index_url}/company_getinfos?'
                para = self.rc.rc_detail_para(com_id,com_name,page)
                hds = self.gh.header()
                hds.update({'Referer': f'{self.index_url}/firm_{com_id}.html'})
                time.sleep(random.randint(1, 2))
                res = requests.get(url,params=para,headers=hds).text
                tree = self.gm.verify(res)
                pub_date_li = tree.xpath('//tbody/tr[position()>1]/td[2]/text()')
                value = self.rc.one_year_judge(pub_date_li)
                if value == False:
                    break
                rc_info_li = tree.xpath('//tbody/tr[position()>1]')
                rc.get_info(rc_info_li,com_id,count)
            value = value
        else:
            print('该企业招聘信息采集结束！')


if __name__ == '__main__':
    rc = RecruitInfo()
    rc.rc_info()
