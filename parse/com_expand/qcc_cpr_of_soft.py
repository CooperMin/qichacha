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

class CprOfSoft():
    def __init__(self):
        self.db = db()
        self.dk = dk()
        self.gh = gh()
        self.tm = tm()
        self.gm = gm()
        self.index_url = 'https://www.qichacha.com'

    def get_com_id(self):
        cos = CprOfSoft()
        # sel = """
        # SELECT `com_id`,`com_name`,`status_cpr_of_soft`,`count_cpr_of_soft`
        # FROM `com_info`
        # WHERE `origin`
        # IS NOT NULL AND LENGTH(`com_id`) = 32
        # AND `status_cpr_of_soft` IS NULL
        # AND `count_cpr_of_soft` != '0'
        # ORDER BY RAND() LIMIT 1;
        # """
        sel = """
        SELECT b.`com_id`,b.`com_name`,b.`status_cpr_of_soft`,b.`count_cpr_of_soft`
        FROM temp_ppp a JOIN com_info b
        ON a.`com_name`=b.`com_name`
        AND LENGTH(b.com_id)=32
        AND b.`status_cpr_of_soft` IS NULL
        AND count_cpr_of_soft != 0
        ORDER BY RAND() LIMIT 1;
        """
        result = cos.db.selsts(sel)
        if result == ():
            result = [None, None, None, None]
        else:
            result = result[0]
        return result

    def get_page_count(self):  # 获取页面页数
        cos = CprOfSoft()
        result = cos.get_com_id()
        com_id = result[0]
        com_name = result[1]

        # com_id = '608886557bb9cf989ae600d1e8a94d40' #测试代码，采集时需注释掉
        # com_name = '网易(杭州)网络有限公司' #测试代码，采集时需注释掉
        key = cos.dk.search_key(com_name)
        status = result[2]
        if com_id == None:
            value = [None, None, None]
        else:
            index_url = 'https://www.qichacha.com'
            com_url = f'{index_url}/company_getinfos?unique={com_id}&companyname={key}&tab=assets'
            hds = cos.gh.header()
            hds.update({'Referer': f'{index_url}/firm_{com_id}.html'})
            time.sleep(random.randint(1, 2))
            res = requests.get(com_url, headers=hds).text
            tree = etree.HTML(res)
            count_cos = tree.xpath('//*[contains(text(),"软件著作权") and @class="title"]/following-sibling::span[@class="tbadge"]/text()')[0].strip()
            if count_cos == '5000+':
                count_page = 500
            else:
                count_cos = int(count_cos)
                if count_cos % 10 == 0:
                    count_page = count_cos // 10
                else:
                    count_page = count_cos // 10 + 1
            value = [com_id, com_name, count_page, index_url]
        return value

    def get_page_info(self): #获取页面详情
        cos = CprOfSoft()
        value = cos.get_page_count()
        com_id = value[0]
        com_name = value[1]
        count_page = value[2]

        # 临时代码，供单次补采数据【001】
        # com_id = 'd02224f92dc49fb497774c88dd2c83c1'
        # com_name = '中译语通文娱科技(青岛)有限公司'
        # count_page = 2
        # 临时代码，供单次补采数据【001】

        if com_id == None:
            pass
        else:
            key = cos.dk.search_key(com_name)
            index_url = value[3]
            count = 0
            start_time = cos.tm.get_localtime() #当前时间
            for page in range(1, count_page + 1): #临时代码，供单次补采数据【001】
            # for page in range(1, count_page + 1):
            #     if page == 1:
            #         page_url = f'https://www.qichacha.com/company_getinfos?unique={com_id}&companyname={com_name}&tab=assets'
                page_url = f'{index_url}/company_getinfos?unique={com_id}&companyname={key}&p={page}&tab=assets&box=rjzzq'
                hds = cos.gh.header()
                hds.update({'Referer': f'{index_url}/firm_{com_id}.html'})
                time.sleep(random.randint(1,2))
                res_pg = requests.get(page_url, headers=hds).text
                tree_pg = cos.gm.verify(res_pg)
                content_li = tree_pg.xpath('//table/tr[position()>1]')
                for content in content_li:
                    count += 1
                    soft_num = content.xpath('td[1]/text()')[0]
                    soft_name = content.xpath('td[2]/text()')[0]
                    try:
                        soft_ver_no = content.xpath('td[3]/text()')[0]
                    except:
                        soft_ver_no = '-'
                    soft_pub_date = content.xpath('td[4]/text()')[0].strip()
                    soft_short_name = content.xpath('td[5]/text()')[0].strip()
                    soft_reg_no = content.xpath('td[6]/text()')[0]
                    reg_approval_date = content.xpath('td[7]/text()')[0]
                    print('\n{0}--总第{1}条----{2}/{3}页--{0}\n'.format('-' * 9, count,page,count_page))
                    localtime = tm().get_localtime()  # 当前时间
                    create_time = localtime
                    print(f'公司ID:{com_id} 当前时间：{localtime}')
                    print(f'公司名称：{com_name}')
                    print(f'序号:{soft_num}\n软件名称:{soft_name}\n版本号:{soft_ver_no}\n发布日期:{soft_pub_date}\n软件简称:{soft_short_name}\n'
                          f'登记号:{soft_reg_no}\n登记批准号:{reg_approval_date}\n')
                    ins = f"""
                    INSERT INTO  
                    `com_cpr_of_soft`
                    (`com_id`,`soft_num`,`soft_name`,`soft_ver_no`,`soft_pub_date`,
                    `soft_short_name`,`soft_reg_no`,`reg_approval_date`,`create_time`)
                    VALUES 
                    ("{com_id}","{soft_num}","{soft_name}","{soft_ver_no}","{soft_pub_date}",
                    "{soft_short_name}","{soft_reg_no}","{reg_approval_date}","{create_time}");
                    """
                    cos.db.inssts(ins)

                    upd = f"""
                    UPDATE 
                    `com_info` 
                    SET
                    `status_cpr_of_soft` = 1
                    WHERE 
                    `com_id` = "{com_id}" ;
                    """
                    cos.db.updsts(upd)
            localtime = cos.tm.get_localtime()  # 当前时间
            print('\n{1}\n{0}数据采集完成!{0}\n{1}'.format('+' * 7, '+' * 25))
            print(f'当前时间：{localtime}\n')
            time.sleep(3)

    #
    # def run(self):
    #     cos = CprOfSoft()
    #     while
    #         print('Loading......\n')
    #         time.sleep(5)
    #         print('开始新一轮采集')
    #         pt.get_page_info()

if __name__ == '__main__':
    cos = CprOfSoft()
    while 1 == 1:
        print('Loading......\n')
        time.sleep(5)
        print('开始新一轮采集')
        cos.get_page_info()