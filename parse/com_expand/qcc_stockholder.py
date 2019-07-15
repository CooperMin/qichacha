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
        self.index_url = 'https://www.qichacha.com'

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
        sel = """
        SELECT `com_id`,`com_name`,`status_stockholder`
        FROM `com_info`
        WHERE `chain` ='虚拟现实'
        AND LENGTH(com_id) > 8
        AND `status_stockholder` IS NULL
        ORDER BY RAND() LIMIT 1;
        """
        # sel = """
        # SELECT `com_id`,`com_name`,`status_stockholder`
        # FROM `com_info`
        # WHERE `com_id` IN
        # (
        # '06b9ede70996255ed343050895046d00',
        # '09a2b97c0596a84cf14404a4bd2c37d5',
        # '18ff2c7ad1d11bfe40e0bec84f6d04d3',
        # '1b16bbdae1540c6a72cd81d918b7c1f6',
        # '30c09ef2def97bd3dc8d021fc2233b05',
        # '31755ff79f6e867d79f7e49cb34da867',
        # '424b1559bdac92d298cf9751979eb26b',
        # '47967ccec9d2e681d6f478e0dd16e0b9',
        # '48431ef3f2c62cc60e1f4c22a178ee50',
        # '4c468b205f73f703274e9db7f769a03f',
        # '5602135acdc60cd54daf58cffbc24367',
        # '61b780963a4bc4df5707fe376e41fb6f',
        # '652177a5d80be3d70d7460a09018f599',
        # '722e57a557a857c16121d5c03bd06d42',
        # '7bb7f10fbffbdb6af869af34e8697ecc',
        # '89d337c3d33410e68ca65d7933bd7d05',
        # '8ad8b2d2c15fb92f9ce14107489e83cd',
        # '9779771217b77e4538bd505660939c9a',
        # '9b0c52e7af1ee199857b94bc3ea6be3d',
        # 'a484e7a0b3167f6b257beb51dd93b241',
        # 'a58533710987ecf98159545b61505a74',
        # 'a5a0ba522ce994fb2a8de3a7625534e1',
        # 'a9aa7de83d5d7b4c5008310395b1f403',
        # 'ad797adc3b0a3fe293a0d7238c671b72',
        # 'af8ef0be6adcc6cc6c5b5d1c217b487c',
        # 'b45f3cc43a98aa52f5b3409cef1d6cd9',
        # 'd3d4ff0894e82ca22a9e6b3a66fda267',
        # 'dbe7a5624002aec7b0f26445c94f60cc',
        # 'e06f5af040745430aec2faf8684ae3c7',
        # 'f11933e8723fd03d325529bd2adc19a6',
        # 'fa078a468930c63c92f7909b5a1c5788',
        # 'ff0e1ff937b7aaa29b8953a54c978fe8'
        # )
        # AND `status_stockholder` IS NULL
        # ORDER BY RAND() LIMIT 1;
        # """
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
        sel = """
        SELECT count(*) FROM `com_info`
        WHERE `chain` ='虚拟现实'
        AND LENGTH(com_id) > 8
        AND `status_stockholder` IS NULL;
        """
        # sel = """
        # SELECT count(*)
        # FROM `com_info`
        # WHERE `com_id` IN
        # (
        # '06b9ede70996255ed343050895046d00',
        # '09a2b97c0596a84cf14404a4bd2c37d5',
        # '18ff2c7ad1d11bfe40e0bec84f6d04d3',
        # '1b16bbdae1540c6a72cd81d918b7c1f6',
        # '30c09ef2def97bd3dc8d021fc2233b05',
        # '31755ff79f6e867d79f7e49cb34da867',
        # '424b1559bdac92d298cf9751979eb26b',
        # '47967ccec9d2e681d6f478e0dd16e0b9',
        # '48431ef3f2c62cc60e1f4c22a178ee50',
        # '4c468b205f73f703274e9db7f769a03f',
        # '5602135acdc60cd54daf58cffbc24367',
        # '61b780963a4bc4df5707fe376e41fb6f',
        # '652177a5d80be3d70d7460a09018f599',
        # '722e57a557a857c16121d5c03bd06d42',
        # '7bb7f10fbffbdb6af869af34e8697ecc',
        # '89d337c3d33410e68ca65d7933bd7d05',
        # '8ad8b2d2c15fb92f9ce14107489e83cd',
        # '9779771217b77e4538bd505660939c9a',
        # '9b0c52e7af1ee199857b94bc3ea6be3d',
        # 'a484e7a0b3167f6b257beb51dd93b241',
        # 'a58533710987ecf98159545b61505a74',
        # 'a5a0ba522ce994fb2a8de3a7625534e1',
        # 'a9aa7de83d5d7b4c5008310395b1f403',
        # 'ad797adc3b0a3fe293a0d7238c671b72',
        # 'af8ef0be6adcc6cc6c5b5d1c217b487c',
        # 'b45f3cc43a98aa52f5b3409cef1d6cd9',
        # 'd3d4ff0894e82ca22a9e6b3a66fda267',
        # 'dbe7a5624002aec7b0f26445c94f60cc',
        # 'e06f5af040745430aec2faf8684ae3c7',
        # 'f11933e8723fd03d325529bd2adc19a6',
        # 'fa078a468930c63c92f7909b5a1c5788',
        # 'ff0e1ff937b7aaa29b8953a54c978fe8'
        # )
        # AND `status_stockholder` IS NULL
        # """
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
                count_sh = tree.xpath('//div[@class="company-nav-items"]/span[contains(text(),"股东信息")]/span/text()|//div[@class="company-nav-items"]/a[@data-pos="partnerslist"]/span/text()')[0]
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
            header.update({'Referer':f'https://www.qichacha.com/firm_{com_id}.html'})
            url = ''.join((sh.index_url,'/company_getinfos?'))
            res = requests.get(url,params=para,headers=header).text
            tree = sh.gm.verify(res)
        return tree

    def parse_info(self,tree,com_id,com_name,page,sh_page_count):
        count = (page - 1) * 50
        if tree == None:
            print('无相关数据！\n')
        else:
            stockholder_li = tree.xpath('//table[contains(@class,"ntable ntable-odd npth")]/tr[position()>1]')
            for stockholder_info in stockholder_li:
                count += 1
                stockholder_num = stockholder_info.xpath('td[1]/text()')[0].strip()
                stockholder_name = stockholder_info.xpath('td[2]//*[@class="seo font-14"]/text()')[0].strip()
                stockholder_rate = stockholder_info.xpath('td[3]/text()')[0].strip()
                subscribed_capital_amount = stockholder_info.xpath('td[4]/text()')[0].strip()
                subscribed_capital_date = stockholder_info.xpath('td[5]/text()')[0].strip()
                try:
                    contributed_capital_amount = stockholder_info.xpath('td[6]/text()')[0].strip()
                except:
                    contributed_capital_amount = '--'
                try:
                    contributed_capital_date = stockholder_info.xpath('td[7]/text()')[0].strip()
                except:
                    contributed_capital_date = '--'
                try:
                    relation_product = stockholder_info.xpath('td[8]/text()')[0].strip()
                except:
                    try:
                        relation_product = stockholder_info.xpath('td[8]/a/text()')[0].strip()
                    except:
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
            for page in range(1, sh_page_count + 1):
                count += 1
                tree = sh.get_page_req(com_id,com_name,page)
                sh.parse_info(tree,com_id,com_name,page,sh_page_count)
                gm().upd_status(com_id, status_column, count_column, count_sh)
                # input('Pause!')
            count_cond = sh.verify_cond()
            print('\n{2}\n{1}剩余{0}家企业股东数据待采集！{1}\n{2}\n'.format(count_cond, '*' * 20, '*' * 63))
        print('\n数据采集完成！')

if __name__ == '__main__':
    sh = StockHolder()
    sh.running()




