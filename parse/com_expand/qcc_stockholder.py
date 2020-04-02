#! /usr/bin/env python3
# -*- coding:utf-8 -*-
"""
企查查股东信息
"""
import time
import random
import requests

from support.others import TimeInfo as tm
from support.use_mysql import ConnMysql as db
from support.headers import GeneralHeaders as gh
from parse.com_common.common import GeneralMethod as gm

class StockHolder():
    def __init__(self):
        self.gh = gh()
        self.db = db()
        self.gm = gm()
        self.tm = tm()
        self.index_url = 'https://www.qcc.com'

    def get_com_id(self):
        sh = StockHolder()
        # sel = """
        # SELECT `com_id`,`com_name`,`status_stockholder`
        # FROM `com_info`
        # WHERE `chain` ='虚拟现实'
        # AND LENGTH(com_id) > 8
        # AND `area` = '广东省'
        # AND `status_stockholder` IS NULL
        # ORDER BY RAND() LIMIT 1;
        # """
        # sel = """
        # SELECT `com_id`,`com_name`,`status_stockholder`
        # FROM `com_info`
        # WHERE `chain` ='虚拟现实'
        # AND LENGTH(com_id) > 8
        # WHERE `status_stockholder` IS NULL
        # ORDER BY RAND() LIMIT 1;
        # """
        # sel = """
        # SELECT `com_id`,`com_name`,`status_stockholder`
        # FROM `com_info`
        # WHERE `com_id` IN
        # (
        # '4420bb5ca97cf5cf455137f279e23e90'
        # )
        # AND `status_stockholder` IS NULL
        # ORDER BY RAND() LIMIT 1;
        # """
        sel = """
        SELECT `com_id`,`com_name`,`status_stockholder`
        FROM `com_info`
        WHERE `other_id` LIKE '%ls1000%'
        AND LENGTH(com_id) = 32
        AND `status_stockholder` IS NULL
        ORDER BY RAND() LIMIT 1;
        """
        result = sh.db.selsts(sel)
        if result == ():
            result = [None, None, None]
        else:
            result = result[0]
        return result

    def get_column(self,sql): #接收sql语句，返回结果
        sh = StockHolder()
        result = sh.db.selsts(sql)[0]
        return result #返回元祖数据

    def verify_cond(self): #验证是否符合继续采集的条件
        sh = StockHolder()
        # sel = """
        # SELECT count(*) FROM `com_info`
        # WHERE `chain` ='虚拟现实'
        # AND LENGTH(com_id) > 8
        # AND `area` = '广东省'
        # AND `status_stockholder` IS NULL;
        # """
        # sel = """
        # SELECT count(*) FROM `com_info`
        # # WHERE `chain` ='虚拟现实'
        # # AND LENGTH(com_id) > 8
        # WHERE `status_stockholder` IS NULL;
        # """
        # sel = """
        # SELECT count(*)
        # FROM `com_info`
        # WHERE `com_id` IN
        # (
        # '4420bb5ca97cf5cf455137f279e23e90'
        # )
        # AND `status_stockholder` IS NULL;
        # """
        sel = """
        SELECT count(*)
        FROM `com_info`
        WHERE `other_id` LIKE '%ls1000%'
        AND LENGTH(com_id) = 32
        AND `status_stockholder` IS NULL;
        """
        result = sh.get_column(sel)[0]
        return result

    def count_sh_judge(self,com_id): #根据公司首页股东信息字段判断股东数量，模糊判断，需做二次判断
        sh = StockHolder()
        header = sh.gh.header()
        if com_id == None:
            count_sh = 0
        else:
            com_url = f'{sh.index_url}/firm_{com_id}.html'
            time.sleep(random.randint(3, 5))
            res = requests.get(com_url,headers=header).text
            tree = sh.gm.verify(res)
            try:
                #可疑点，count_sh，20191122 测试，此行可删除
                # count_sh = tree.xpath('//div[@class="company-nav-items"]/span[contains(text(),"股东信息")]/span/text()')[0].strip()
                # count_sh = tree.xpath('//div[@class="company-nav-items"]/a[@data-pos="partnern"]/span/text()')[0].strip()
                count_sh = tree.xpath('//div[@class="company-nav-items"]/span[contains(text(),"股东信息")]/span/text()|//div[@class="company-nav-items"]/a[@data-pos="partnern"]/span/text()')[0].strip()
                # count_sh = tree.xpath('//div[@class="company-nav-items"]/span[contains(text(),"股东信息")]/span/text()|//div[@class="company-nav-items"]/a[@data-pos="partnerslist"]/span/text()')[0]
                if count_sh == '999+':
                    count_sh = 999
                count_sh = int(count_sh)
            except:
                count_sh = 0
        status_column = 'status_stockholder'
        count_column = 'count_stockholder'
        # gm().upd_status(com_id, status_column, count_column, count_sh)
        return count_sh

    def sh_page_judge(self,count_sh): #判断页码                                                           #判断是否是最近一或两年的招聘数据
        if count_sh == 0:
            sh_page_count = 0
        else:
            if count_sh % 50 == 0:
                sh_page_count = count_sh // 50
            else:
                sh_page_count = count_sh // 50 + 1
        return sh_page_count

    def sh_detail_para(self,com_id,com_name,page): #详情页链接参数
        para = {
            'unique': f'{com_id}',
            'companyname': f'{com_name}',
            'p': page,
            'tab': 'base',
            'box': 'partners'
        }
        return para

    def get_page_req(self,com_id,com_name,page):
        sh = StockHolder()
        if page == 0:
            tree = None
        else:
            para = sh.sh_detail_para(com_id,com_name,page)
            header = sh.gh.header()
            header.update({'Referer':f'https://www.qcc.com/firm_{com_id}.html'})
            url = ''.join((sh.index_url,'/company_getinfos?'))
            res = requests.get(url,params=para,headers=header).text
            tree = sh.gm.verify(res)
        return tree

    def verify_stockholder_args(self,tree):
        stockholder_args = tree.xpath('//table[contains(@class,"ntable ntable-odd npth")]/tbody/tr[1]/th/text()')
        if len(stockholder_args) == 0:
            stockholder_args = tree.xpath('//table[contains(@class,"ntable ntable-odd npth")]/tr[1]/th/text()')
        return stockholder_args

    def parse_info(self,tree,com_id,com_name,page,sh_page_count):
        sh = StockHolder()
        count = (page - 1) * 50
        if tree == None:
            print('无相关数据！\n')
        else:
            # 引入verify_stockholder_args方法 -- 2019-11-26
            stockholder_args = sh.verify_stockholder_args(tree)
            stockholder_li = tree.xpath('//table[contains(@class,"ntable ntable-odd npth")]/tr[position()>1]|//table[contains(@class,"ntable ntable-odd npth")]/tbody/tr[position()>1]')
            for stockholder_info in stockholder_li:
                count += 1
                stockholder_num = stockholder_info.xpath('td[1]/text()')[0].strip()
                stockholder_name = stockholder_info.xpath('td[2]//*[@class="seo font-14"]/text()')[0].strip()
                if stockholder_info.xpath('td[3]/text()')[0].strip() == '':
                    stockholder_rate = stockholder_info.xpath('td[3]/span/text()')[0].strip()
                else:
                    stockholder_rate = stockholder_info.xpath('td[3]/text()')[0].strip()
                if '最终受益股份' not in stockholder_args:
                    if stockholder_info.xpath('td[4]/text()')[0].strip() == '':
                        subscribed_capital_amount = stockholder_info.xpath('td[4]/span/text()')[0].strip()
                    else:
                        subscribed_capital_amount = stockholder_info.xpath('td[4]/text()')[0].strip()
                    if stockholder_info.xpath('td[5]/text()')[0].strip() == '':
                        subscribed_capital_date = stockholder_info.xpath('td[5]/span/text()')[0].strip()
                    else:
                        subscribed_capital_date = stockholder_info.xpath('td[5]/text()')[0].strip()
                else:
                    if stockholder_info.xpath('td[5]/text()')[0].strip() == '':
                        subscribed_capital_amount = stockholder_info.xpath('td[5]/span/text()')[0].strip()
                    else:
                        subscribed_capital_amount = stockholder_info.xpath('td[5]/text()')[0].strip()
                    if stockholder_info.xpath('td[6]/text()')[0].strip() == '':
                        subscribed_capital_date = stockholder_info.xpath('td[6]/span/text()')[0].strip()
                    else:
                        subscribed_capital_date = stockholder_info.xpath('td[6]/text()')[0].strip()
                if '实缴出资额' not in stockholder_args:
                    contributed_capital_amount = '--'
                    contributed_capital_date = '--'
                else:
                    if '最终受益股份' not in stockholder_args:
                        if stockholder_info.xpath('td[6]/text()')[0].strip() == '':
                            contributed_capital_amount = stockholder_info.xpath('td[6]/span/text()')[0].strip()
                            contributed_capital_date = stockholder_info.xpath('td[7]/span/text()')[0].strip()
                        else:
                            contributed_capital_amount = stockholder_info.xpath('td[6]/text()')[0].strip()
                            contributed_capital_date = stockholder_info.xpath('td[7]/text()')[0].strip()
                    else:
                        if stockholder_info.xpath('td[7]/text()')[0].strip() == '':
                            contributed_capital_amount = stockholder_info.xpath('td[7]/span/text()')[0].strip()
                            contributed_capital_date = stockholder_info.xpath('td[8]/span/text()')[0].strip()
                        else:
                            contributed_capital_amount = stockholder_info.xpath('td[7]/text()')[0].strip()
                            contributed_capital_date = stockholder_info.xpath('td[8]/text()')[0].strip()
                if '关联产品/机构' in stockholder_args:
                    if '最终受益股份' not in stockholder_args and '实缴出资额' not in stockholder_args:
                        if stockholder_info.xpath('td[6]/text()')[0].strip() == '':
                            relation_product = stockholder_info.xpath('td[6]/a/text()')[0].strip()
                        else:
                            relation_product = stockholder_info.xpath('td[6]/text()')[0].strip()
                    elif '最终受益股份' not in stockholder_args and '实缴出资额' in stockholder_args:
                        if stockholder_info.xpath('td[8]/text()')[0].strip() == '':
                            relation_product = stockholder_info.xpath('td[8]/a/text()')[0].strip()
                        else:
                            relation_product = stockholder_info.xpath('td[8]/text()')[0].strip()
                    elif '最终受益股份' in stockholder_args and '实缴出资额' not in stockholder_args:
                        if stockholder_info.xpath('td[7]/text()')[0].strip() == '':
                            relation_product = stockholder_info.xpath('td[7]/a/text()')[0].strip()
                        else:
                            relation_product = stockholder_info.xpath('td[7]/text()')[0].strip()
                    else:
                        if stockholder_info.xpath('td[9]/text()')[0].strip() == '':
                            relation_product = stockholder_info.xpath('td[9]/a/text()')[0].strip()
                        else:
                            relation_product = stockholder_info.xpath('td[9]/text()')[0].strip()
                else:
                    relation_product = '--'
                localtime = tm().get_localtime()  # 当前时间
                create_time = localtime
                print('\n{0}--总第{1}条----第{2}/{3}页----{0}\n'.format('-' * 9, count, page,sh_page_count))
                print(f'当前时间：{create_time}')
                print(f'公司ID:{com_id}\n公司名称:{com_name}')
                print(f'序号:{stockholder_num}\n股东:{stockholder_name}\n持股比例:{stockholder_rate}\n认缴出资额:{subscribed_capital_amount}\n认缴出资日期:{subscribed_capital_date}\n'
                      f'实缴出资额:{contributed_capital_amount}\n实缴出资日期:{contributed_capital_date}\n关联产品/机构:{relation_product}\n')
                ins = f"""
                INSERT INTO `com_stockholder`
                (com_id,stockholder_num,stockholder_name,stockholder_rate,subscribed_capital_amount,
                subscribed_capital_date,contributed_capital_amount,contributed_capital_date,relation_product,create_time)
                VALUES 
                ("{com_id}","{stockholder_num}","{stockholder_name}","{stockholder_rate}","{subscribed_capital_amount}",
                "{subscribed_capital_date}","{contributed_capital_amount}","{contributed_capital_date}","{relation_product}","{create_time}");
                """
                # udp = f"""
                # UPDATE `com_info`
                # SET `status_stockholder` = "9"
                # AND `count_stockholder` = "{count_sh}"
                # WHERE `com_id` = "{com_id}";"""
                self.db.inssts(ins)
                # sh.db.updsts(udp)

    def running(self):
        sh = StockHolder()
        count_cond = sh.verify_cond()
        count = 0
        print('\n{2}\n{1}剩余{0}家企业股东数据待采集！{1}\n{2}\n'.format(count_cond, '*' * 20, '*' * 63))
        while count_cond > 0:
            print('Loading......\n')
            time.sleep(3)
            print('开始新一轮采集')
            result = sh.get_com_id()
            com_id = result[0]
            com_name = result[1]
            count_sh = sh.count_sh_judge(com_id)
            status_column = 'status_stockholder'
            count_column = 'count_stockholder'
            # sh.gm.upd_status(com_id, status_column, count_column, count_sh)
            sh_page_count = sh.sh_page_judge(count_sh)
            if sh_page_count == 0:
                print('无相关数据呢！\n')
                count += 1
                gm().upd_status(com_id, status_column, count_column, count_sh)
            else:
                for page in range(1, sh_page_count + 1):
                    count += 1
                    tree = sh.get_page_req(com_id,com_name,page)
                    sh.parse_info(tree,com_id,com_name,page,sh_page_count)
                    gm().upd_status(com_id, status_column, count_column, count_sh)
            count_cond = sh.verify_cond()
            print('\n{2}\n{1}剩余{0}家企业股东数据待采集！{1}\n{2}\n'.format(count_cond, '*' * 20, '*' * 63))
        print('\n数据采集完成！')

if __name__ == '__main__':
    sh = StockHolder()
    sh.running()




