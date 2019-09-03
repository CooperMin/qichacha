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

class WokrsInfo():
    def __init__(self):
        self.db = db()
        self.dk = dk()
        self.gh = gh()
        self.tm = tm()
        self.gm = gm()
        self.index_url = 'https://www.qichacha.com'

    def get_com_id(self):
        wi = WokrsInfo()
        # sel = """
        # SELECT `com_id`,`com_name`,`status_cpr_of_works`,`count_cpr_of_works`
        # FROM `com_info`
        # WHERE `origin`
        # IS NOT NULL AND LENGTH(`com_id`) = 32
        # AND `status_cpr_of_works` IS NULL
        # AND `count_cpr_of_works` != '0'
        # ORDER BY RAND() LIMIT 1;
        # """
        sel = """
        SELECT b.`com_id`,b.`com_name`,b.`status_cpr_of_works`,b.`count_cpr_of_works`
        FROM temp_ppp a JOIN com_info b
        ON a.`com_name`=b.`com_name`
        AND LENGTH(b.com_id)=32
        AND b.`status_cpr_of_works` IS NULL
        AND count_cpr_of_works != 0
        ORDER BY RAND() LIMIT 1;
        """
        result = wi.db.selsts(sel)
        if result == ():
            result = [None, None, None, None]
        else:
            result = result[0]
        return result

    def get_column(self,sql): #接收sql语句，返回结果
        wi = WokrsInfo()
        result = wi.db.selsts(sql)[0]
        return result #返回元祖数据

    def get_page_count(self):  # 获取页面页数
        wi = WokrsInfo()
        result = wi.get_com_id()
        com_id = result[0]
        com_name = result[1]

        # com_id = '608886557bb9cf989ae600d1e8a94d40' #测试代码，采集时需注释掉
        # com_name = '网易(杭州)网络有限公司' #测试代码，采集时需注释掉
        key = wi.dk.search_key(com_name)
        status = result[2]
        if com_id == None:
            value = [None, None, None]
        else:
            index_url = 'https://www.qichacha.com'
            com_url = f'{index_url}/company_getinfos?unique={com_id}&companyname={key}&tab=zzq'
            hds = wi.gh.header()
            hds.update({'Referer': f'{index_url}/firm_{com_id}.html'})
            time.sleep(random.randint(1, 2))
            res = requests.get(com_url, headers=hds).text
            tree = wi.gm.verify(res)
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
        wi = WokrsInfo()
        value = wi.get_page_count()
        com_id = value[0]
        com_name = value[1]
        count_page = value[2]

        # 临时代码，供单次补采数据【001】
        # com_id = '6fac25ffb0a99a91efb6cd0942be4353'
        # com_name = '青岛雷神科技股份有限公司'
        # count_page = 2
        # 临时代码，供单次补采数据【001】

        if com_id == None:
            pass
        else:
            key = wi.dk.search_key(com_name)
            index_url = value[3]
            count = 0
            start_time = wi.tm.get_localtime() #当前时间
            for page in range(1, count_page + 1): #临时代码，供单次补采数据【001】
            # for page in range(1, count_page + 1):
            #     if page == 1:
            #         page_url = f'https://www.qichacha.com/company_getinfos?unique={com_id}&companyname={com_name}&tab=assets'
                page_url = f'{index_url}/company_getinfos?unique={com_id}&companyname={key}&p={page}&tab=assets&box=zzq'
                hds = wi.gh.header()
                hds.update({'Referer': f'{index_url}/firm_{com_id}.html'})
                time.sleep(random.randint(1,2))
                res_pg = requests.get(page_url, headers=hds).text
                tree_pg = wi.gm.verify(res_pg)
                content_li = tree_pg.xpath('//table/tr[position()>1]')
                for content in content_li:
                    count += 1
                    work_num = content.xpath('td[1]/text()')[0]
                    work_name = content.xpath('td[2]/text()')[0].strip()
                    work_pub_date = content.xpath('td[3]/text()')[0].strip()
                    create_finish_date = content.xpath('td[4]/text()')[0].strip()
                    work_reg_no = content.xpath('td[5]/text()')[0]
                    work_reg_date = content.xpath('td[6]/text()')[0]
                    reg_type = content.xpath('td[7]/text()')[0].strip()
                    print('\n{0}--总第{1}条----{2}/{3}页--{0}\n'.format('-' * 9, count,page,count_page))
                    localtime = wi.tm.get_localtime()  # 当前时间
                    create_time = localtime
                    print(f'公司ID:{com_id} 当前时间：{localtime}')
                    print(f'公司名称：{com_name}\n序号：{work_num}\n作品名称:{work_name}')
                    print(f'首次发表日期:{work_pub_date}\n创作完成日期:{create_finish_date}\n登记号:{work_reg_no}\n登记日期:{work_reg_date}\n登记类别:{reg_type}\n')
                    ins = f"""
                    INSERT INTO
                    `com_cpr_of_works`
                    (`com_id`,`work_num`,`work_name`,`work_pub_date`,`create_finish_date`,
                    `work_reg_no`,`work_reg_date`,`reg_type`,`create_time`)
                    VALUES
                    ("{com_id}","{work_num}","{work_name}","{work_pub_date}","{create_finish_date}",
                    "{work_reg_no}","{work_reg_date}","{reg_type}","{create_time}");
                    """
                    wi.db.inssts(ins)

                    upd = f"""
                    UPDATE
                    `com_info`
                    SET
                    `status_cpr_of_works` = 1
                    WHERE
                    `com_id` = "{com_id}" ;
                    """
                    wi.db.updsts(upd)
            localtime = wi.tm.get_localtime()  # 当前时间
            print('\n{1}\n{0}数据采集完成!{0}\n{1}'.format('+' * 7, '+' * 25))
            print(f'当前时间：{localtime}\n')
            time.sleep(3)

    def verify_cond(self):#验证是否符合继续采集的条件
        wi = WokrsInfo()
        # sel = """
        # SELECT COUNT(*) FROM `com_info`
        # WHERE `origin` IS NOT NULL
        # AND LENGTH(`com_id`) = 32
        # AND `status_cpr_of_works` IS NULL
        # AND `count_cpr_of_works` != '0';
        # """
        sel = """
        SELECT COUNT(*)
        FROM temp_ppp a JOIN com_info b
        ON a.`com_name`=b.`com_name`
        AND LENGTH(b.com_id)=32
        AND b.`status_cpr_of_works` IS NULL
        AND count_cpr_of_works != 0;
        """
        result = wi.get_column(sel)[0]
        return result

    def run_web(self):
        wi = WokrsInfo()
        count_cond = wi.verify_cond()
        print('\n{2}\n{1}剩余{0}家企业作品著作权数据待采集！{1}\n{2}\n'.format(count_cond, '*' * 20, '*' * 63))
        while count_cond > 0:
            print('Loading......\n')
            time.sleep(3)
            print('开始新一轮采集')
            wi.get_page_info()
            time.sleep(3)
            count_cond = wi.verify_cond()
            print('\n{2}\n{1}剩余{0}家企业作品著作权数据待采集！{1}\n{2}\n'.format(count_cond, '*' * 20, '*' * 63))
        print('\n数据采集完成！')

if __name__ == '__main__':
    wi = WokrsInfo()
    wi.run_web()