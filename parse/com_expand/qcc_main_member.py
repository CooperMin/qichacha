#! /usr/bin/env python3
# -*- coding:utf-8 -*-
"""
企查查-核心成员信息采集
"""
import time
import random
import requests

from support.others import TimeInfo as tm
from support.use_mysql import ConnMysql as db
from support.headers import GeneralHeaders as gh
from parse.com_common.common import GeneralMethod as gm
class MainMember():
    def __init__(self):
        self.gh = gh()
        self.db = db()
        self.gm = gm()
        self.tm = tm()
        self.index_url = 'https://www.qichacha.com'

    def get_com_id(self):
        mm = MainMember()
        # sel = """
        # SELECT `com_id`,`com_name`,`status_main_member`
        # FROM `com_info`
        # WHERE `chain` ='虚拟现实'
        # AND LENGTH(com_id) > 8
        # AND `area` = '广东省'
        # AND `status_main_member` IS NULL
        # ORDER BY RAND() LIMIT 1;
        # """
        # sel = """
        # SELECT `com_id`,`com_name`,`status_main_member`
        # FROM `com_info`
        # WHERE `com_id` IN
        # (
        # '9cb20e0fb07d9f3c5a5f6bba4134dc95',
        # '69c2502236fb0bf57ce6ce677feef355'
        # )
        # AND `status_main_member` IS NULL
        # ORDER BY RAND() LIMIT 1;
        # """
        sel = """
        SELECT `com_id`,`com_name`,`status_main_member`
        FROM `com_info`
        WHERE `other_id` LIKE '%ls1000%'
        AND LENGTH(`com_id`) = 32
        AND `status_main_member` IS NULL
        ORDER BY RAND() LIMIT 1;
        """
        result = mm.db.selsts(sel)
        if result == ():
            result = [None, None, None]
        else:
            result = result[0]
        return result

    def get_column(self,sql): #接收sql语句，返回结果
        mm = MainMember()
        result = mm.db.selsts(sql)[0]
        return result #返回元祖数据

    def verify_cond(self): #验证是否符合继续采集的条件
        mm = MainMember()
        # sel = """
        # SELECT count(*) FROM `com_info`
        # WHERE `chain` ='虚拟现实'
        # AND LENGTH(com_id) > 8
        # AND `area` = '广东省'
        # AND `status_main_member` IS NULL;
        # """
        # sel = """
        # SELECT count(*)
        # FROM `com_info`
        # WHERE `com_id` IN
        # (
        # '9cb20e0fb07d9f3c5a5f6bba4134dc95',
        # '69c2502236fb0bf57ce6ce677feef355'
        # )
        # AND `status_main_member` IS NULL;
        # """
        sel = """
        SELECT count(*)
        FROM `com_info`
        WHERE `other_id` LIKE '%ls1000%'
        AND LENGTH(`com_id`) = 32
        AND `status_main_member` IS NULL;
        """
        result = mm.get_column(sel)[0]
        return result

    def count_cm_judge(self,com_id): #根据公司首页股东信息字段判断股东数量
        mm = MainMember()
        header = mm.gh.header()
        if com_id == None:
            count_mm = 0
            tree = None
        else:
            com_url = f'{mm.index_url}/firm_{com_id}.html'
            time.sleep(random.randint(3, 5))
            res = requests.get(com_url,headers=header).text
            tree = mm.gm.verify(res)
            try:
                count_mm = tree.xpath('//div[@class="company-nav-items"]/span[contains(text(),"核心人员")]/span/text()|//div[@class="company-nav-items"]/a[@data-pos="Mainmember"]/span/text()')[0]
                if count_mm == '999+':
                    count_mm = 999
                count_mm = int(count_mm)
            except:
                count_mm = 0
        return count_mm,tree

    def parse_info(self,com_id,tree): #解析页面内容，获取相关数据
        if tree == None:
            print('无相关数据！')
        else:
            member_li = tree.xpath('//section[@id="Mainmember"]/table[contains(@class,"ntable ntable-odd")]/tr[position()>1]')
            count = 0
            for member_info in member_li:
                count += 1
                member_num = member_info.xpath('td[1]/text()')[0].strip()
                member_name = member_info.xpath('td[2]//*[@class="seo font-14"]/text()')[0].strip()
                member_post = member_info.xpath('td[3]/text()')[0].strip()
                localtime = tm().get_localtime()  # 当前时间
                create_time = localtime
                print('\n{0}--总第{1}条----{0}\n'.format('-' * 9, count))
                print(f'当前时间：{create_time}')
                print(f'公司ID:{com_id}\n序号:{member_num}\n姓名:{member_name}\n职务:{member_post}\n')
                ins = f"""
                INSERT INTO `com_main_member`
                (com_id,member_num,member_name,member_post,create_time)
                VALUES 
                ("{com_id}","{member_num}","{member_name}","{member_post}","{create_time}");
                """
                self.db.inssts(ins)

    def running(self): #执行该方法使程序整体运行
        mm = MainMember()
        count_cond = mm.verify_cond()
        print('\n{2}\n{1}剩余{0}家企业主要人员数据待采集！{1}\n{2}\n'.format(count_cond, '*' * 20, '*' * 63))
        while count_cond > 0:
            print('Loading......\n')
            time.sleep(3)
            print('开始新一轮采集')
            result = mm.get_com_id()
            com_id = result[0]
            info = mm.count_cm_judge(com_id)
            count_mm = info[0]
            tree = info[1]
            mm.parse_info(com_id,tree)
            status_column = 'status_main_member'
            count_column = 'count_main_member'
            gm().upd_status(com_id,status_column,count_column,count_mm)
            count_cond = mm.verify_cond()
            print('\n{2}\n{1}剩余{0}家企业主要人员数据待采集！{1}\n{2}\n'.format(count_cond, '*' * 20, '*' * 63))
        print('\n数据采集完成！')


if __name__ == '__main__':
    mm = MainMember()
    mm.running()







