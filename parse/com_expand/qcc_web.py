#! /usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import time
import random
import requests

from lxml import etree

from support.use_mysql import ConnMysql as db
from support.others import DealKey as dk
from support.others import TimeInfo as tm
from support.headers import GeneralHeaders as gh
from parse.com_common.common import GeneralMethod as gm

class WebSite():
    def __init__(self):
        self.db = db()
        self.dk = dk()
        self.gh = gh()
        self.tm = tm()
        self.gm = gm()
        self.index_url = 'https://www.qcc.com'

    def get_com_id(self):
        ws = WebSite()
        # sel = """
        # SELECT `com_id`,`com_name`,`status_web`,`count_web`
        # FROM `com_info`
        # WHERE `origin`
        # IS NOT NULL AND LENGTH(`com_id`) = 32
        # AND `status_web` IS NULL
        # AND `count_web` != '0'
        # ORDER BY RAND() LIMIT 1;
        # """
        # sel = """
        # SELECT b.`com_id`,b.`com_name`,b.`status_web`,b.`count_web`
        # FROM temp_ppp a JOIN com_info b
        # ON a.`com_name`=b.`com_name`
        # AND LENGTH(b.com_id)=32
        # AND b.`status_web` IS NULL
        # AND count_web != 0
        # ORDER BY RAND() LIMIT 1;
        # """
        sel = """
        SELECT `com_id`,`com_name`,`status_web`,`count_web`
        FROM `com_info`
        WHERE `other_id` LIKE '%ls1000%'
        AND LENGTH(`com_id`) = 32
        AND `status_web` IS NULL
        AND `count_web` != '0'
        ORDER BY RAND() LIMIT 1;
        """
        result = ws.db.selsts(sel)
        if result == ():
            result = [None, None, None, None]
        else:
            result = result[0]
        return result

    def get_column(self,sql): #接收sql语句，返回结果
        ws = WebSite()
        result = ws.db.selsts(sql)[0]
        return result #返回元祖数据

    def get_page_count(self):  # 获取页面页数
        ws = WebSite()
        result = ws.get_com_id()
        com_id = result[0]
        com_name = result[1]

        # com_id = '608886557bb9cf989ae600d1e8a94d40' #测试代码，采集时需注释掉
        # com_name = '网易(杭州)网络有限公司' #测试代码，采集时需注释掉
        key = ws.dk.search_key(com_name)
        status = result[2]
        if com_id == None:
            value = [None, None, None]
        else:
            index_url = 'https://www.qcc.com'
            com_url = f'{index_url}/company_getinfos?unique={com_id}&companyname={key}&tab=website'
            hds = ws.gh.header()
            hds.update({'Referer': f'{index_url}/firm_{com_id}.html'})
            time.sleep(random.randint(1, 2))
            res = requests.get(com_url, headers=hds).text
            tree = ws.gm.verify(res)
            count_web = tree.xpath('//span[@class="tbadge"]/text()')[0].strip()
            if count_web == '5000+':
                count_page = 500
            else:
                count_web = int(count_web)
                if count_web % 10 == 0:
                    count_page = count_web // 10
                else:
                    count_page = count_web // 10 + 1
            value = [com_id, com_name, count_page, index_url]
        return value

    def get_page_info(self): #获取页面详情
        ws = WebSite()
        value = ws.get_page_count()
        com_id = value[0]
        com_name = value[1]
        count_page = value[2]

        # 临时代码，供单次补采数据【001】
        # com_id = 'f1c5372005e04ba99175d5fd3db7b8fc'
        # com_name = '深圳市腾讯计算机系统有限公司'
        # count_page = 45
        # 临时代码，供单次补采数据【001】

        if com_id == None:
            pass
        else:
            key = ws.dk.search_key(com_name)
            index_url = value[3]
            count = 0
            start_time = ws.tm.get_localtime() #当前时间
            for page in range(1, count_page + 1): #临时代码，供单次补采数据【001】
            # for page in range(1, count_page + 1):
            #     if page == 1:
            #         page_url = f'https://www.qichacha.com/company_getinfos?unique={com_id}&companyname={com_name}&tab=assets'
                page_url = f'{index_url}/company_getinfos?unique={com_id}&companyname={key}&p={page}&tab=assets&box=website'
                hds = ws.gh.header()
                hds.update({'Referer': f'{index_url}/firm_{com_id}.html'})
                time.sleep(random.randint(1,2))
                res_pg = requests.get(page_url, headers=hds).text
                tree_pg = ws.gm.verify(res_pg)
                content_li = tree_pg.xpath('//table/tr[position()>1]')
                for content in content_li:
                    count += 1
                    web_num = content.xpath('td[1]/text()')[0]
                    web_name = content.xpath('td[2]/text()')[0]
                    web_site = content.xpath('td[3]/a/text()')
                    if len(web_site) > 1:
                        web_site = web_site
                    elif len(web_site) == 0:
                        web_site = '-'
                    else:
                        web_site = web_site[0]
                    domain_name = content.xpath('td[4]/text()')[0].split('\n')
                    if len(domain_name) > 2:
                        domain_name_li = []
                        for domain in domain_name:
                            if domain != '':
                                domain = domain.strip()
                                domain_name_li.append(domain)
                            else:
                                pass
                        domain_name = domain_name_li
                    else:
                        domain_name = domain_name[1].strip()
                    icp = content.xpath('td[5]/text()')[0].strip()
                    approved_date = content.xpath('td[6]/text()')[0]
                    print('\n{0}--总第{1}条----{2}/{3}页--{0}\n'.format('-' * 9, count,page,count_page))
                    localtime = tm().get_localtime()  # 当前时间
                    create_time = localtime
                    print(f'公司ID:{com_id} 当前时间：{localtime}')
                    print(f'公司名称：{com_name}\n序号：{web_num}')
                    print(f'网站名称:{web_name}\n网址:{web_site}\n域名:{domain_name}\n网站备案/许可证号:{icp}\n审核日期:{approved_date}\n')
                    ins = f"""
                    INSERT INTO
                    `com_web`
                    (`com_id`,`web_num`,`web_name`,`web_site`,`domain_name`,
                    `icp`,`approved_date`,`create_time`)
                    VALUES
                    ("{com_id}","{web_num}","{web_name}","{web_site}","{domain_name}",
                    "{icp}","{approved_date}","{create_time}");
                    """
                    db().inssts(ins)

                    upd = f"""
                    UPDATE
                    `com_info`
                    SET
                    `status_web` = 1
                    WHERE
                    `com_id` = "{com_id}" ;
                    """
                    db().updsts(upd)
            localtime = tm().get_localtime()  # 当前时间
            print('\n{1}\n{0}数据采集完成!{0}\n{1}'.format('+' * 7, '+' * 25))
            print(f'当前时间：{localtime}\n')
            time.sleep(3)

    def verify_cond(self):#验证是否符合继续采集的条件
        ws = WebSite()
        # sel = """
        # SELECT COUNT(*) FROM `com_info`
        # WHERE `origin` IS NOT NULL
        # AND LENGTH(`com_id`) = 32
        # AND `status_web` IS NULL
        # AND `count_web` != '0';
        # """
        # sel = """
        # SELECT COUNT(*)
        # FROM temp_ppp a JOIN com_info b
        # ON a.`com_name`=b.`com_name`
        # AND LENGTH(b.com_id)=32
        # AND b.`status_web` IS NULL
        # AND count_web != 0;
        # """
        sel = """
        SELECT COUNT(*)
        FROM `com_info`
        WHERE `other_id` LIKE '%ls1000%'
        AND LENGTH(`com_id`) = 32
        AND `status_web` IS NULL
        AND `count_web` != '0'
        ORDER BY RAND() LIMIT 1;
        """
        result = ws.get_column(sel)[0]
        return result

    def run_web(self):
        ws = WebSite()
        count_cond = ws.verify_cond()
        print('\n{2}\n{1}剩余{0}家企业网站信息数据待采集！{1}\n{2}\n'.format(count_cond, '*' * 20, '*' * 63))
        while count_cond > 0:
            print('Loading......\n')
            time.sleep(3)
            print('开始新一轮采集')
            ws.get_page_info()
            time.sleep(3)
            count_cond = ws.verify_cond()
            print('\n{2}\n{1}剩余{0}家企业网站信息数据待采集！{1}\n{2}\n'.format(count_cond, '*' * 20, '*' * 63))
        print('\n数据采集完成！')

if __name__ == '__main__':
    ws = WebSite()
    ws.run_web()