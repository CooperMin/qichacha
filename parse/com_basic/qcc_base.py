#! /usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import requests

from support.mysql import QccMysql as db
from support.others import DealKey as dk
from support.others import TimeInfo as tm
from support.headers import GeneralHeaders as gh
from parse.com_common.common import GeneralMethod as gm

class ComBase():
    def __init__(self):
        self.db = db()
        self.gh = gh()
        self.tm = tm()
        self.gm = gm()
        self.index_url = 'https://www.qichacha.com'

    def set_method(self):
        mth1 = 0
        mth2 = 1
        return mth1,mth2

    def sel_sql(self):
        sel = """
        SELECT * FROM `com_info` 
        WHERE 'kw' IS NOT NULL 
        AND 'com_id' IS NULL
        ORDER BY RAND() LIMIT 1;
        """
        return sel

    def get_com_li(self): #读取文件，获取公司列表
        com_file = os.path.abspath(os.path.join(os.getcwd(),'../../doc/company_list'))
        with open(com_file, 'r', encoding='utf-8') as rf:
            rf = rf.readlines()
        com_li = []
        for company in rf:
            company = company.strip()
            com_li.append(company)
        return com_li

    def get_com_name(self,sql):
        cb = ComBase()
        com_name = cb.db.inssts(sql)
        return com_name

    def com_search(self,com_name): #根据关键词/公司名称检索匹配最优公司
        cb = ComBase()
        header = cb.gh.header()
        parm = dk.search_key(com_name)
        url_search = f'https://www.qichacha.com/search?key={parm}'
        res = requests.get(url_search,headers=header).text
        cb.tm.random_sec()
        tree = cb.gm.verify(res)
        kw = com_name.replace('（', '(').replace('）', ')')
        if tree == None:
            com_id = None
            com_url = None
            pass
        else:
            index_url = 'https://www.qichacha.com'
            try:
                com_link = tree.xpath('//*[@id="search-result"]/tr[1]/td[2]/a[@class="ma_h1"]/@href')[0]  # 获取检索结果，匹配与所给公司名称最接近的公司的链接
            except:
                com_link = tree.xpath('//*[@id="search-result"]/tr[1]/td[3]/a[@class="ma_h1"]/@href')[0]  # 获取检索结果，匹配与所给公司名称最接近的公司的链接
            com_id = re.findall(r'(?<=/firm_)(.*)(?=\.html)', com_link)[0]
            com_url = ''.join((index_url, com_link))  # 拼接为完整链接
        return com_id,kw,com_url,url_search

    def req_com_page(self,com_id,kw,com_url,url_search): #返回公司信息页源码
        cb = ComBase()
        header = cb.gh.header()
        header.update({'Referer':f'{url_search}'})
        res = requests.get(com_url, headers=header).text
        cb.tm.random_sec()
        tree = cb.gm.verify(res)
        return tree,com_id,kw

    def verify_com_type(self,tree): #判断公司类型（如是否是上市公司、高新技术企业、社会组织等）
        if tree == None:
            tag_status = -1
            is_listed = -1
            is_hthr = -1
            org_status = -1
        else:
            com_tags = tree.xpath('//div[@class="row tags"]/span/@class')
            if len(com_tags) != 0: #一版为国家机关部门（如国务院、烟草局等）
                tag_status = True
            else:
                tag_status = False
            if 'ntag text-list' in com_tags: #是否上市公司
                is_listed = True
            else:
                is_listed = False
            if 'ntag text-primary' in com_tags: #是否高新技术企业
                is_hthr = True
            else:
                is_hthr = False
            if 'ntag text-pl' in com_tags: #判断机构类型（如：港澳台公司、学校、律师事务所、基金会等）
                org_status = True
            else:
                org_status = False
            if 'ntag text-so' in com_tags: #是否社会组织（如：研究院等）
                so_status = True
            else:
                so_status = False
            print(com_tags)
            input('\nPause')
        return tag_status,is_listed,is_hthr,org_status

    def

    def parse_com_info_comm(self,tree,res,com_id,kw): #解析公司基本信息等
        com_name = tree.xpath('//input[@name="toCompanyName"]/@value')[0].strip()
        try:
            tel = tree.xpath('//span[contains(text(),"电话：") and @class="cdes"]/following-sibling::span[1]/span')[0].text.strip()  # 电话
        except:
            tel = tree.xpath('//span[contains(text(),"电话：") and @class="cdes"]/following-sibling::span[1]')[0].text.strip()  # 电话
        try:
            email = tree.xpath('//span[contains(text(),"邮箱：")]/following-sibling::span[1]/a')[0].text.strip()  # 邮箱
        except:
            email = tree.xpath('//span[contains(text(),"邮箱：")]/following-sibling::span[1]')[0].text.strip()  # 邮箱
        try:
            site = tree.xpath('//span[contains(text(),"官网：")]/following-sibling::span[1]/a')[0].text.strip()  # 官网
        except:
            site = tree.xpath('//span[contains(text(),"官网：")]/following-sibling::span[1]')[0].text.strip()  # 官网
        try:
            try:
                address = tree.xpath('//span[contains(text(),"地址：")]/following-sibling::span[1]/a')[0].text.strip()  # 地址
            except:
                address = tree.xpath('//span[contains(text(),"地址：")]/following-sibling::span[1]')[0].text.strip()
        except:
            address = tree.xpath('//span[contains(text(),"地址：")]/parent/span[2]/a[1]')[0].text.strip()  # 地址
        try:
            business_term = tree.xpath('//td[contains(text(),"注册资本") and @class="tb"]/following-sibling::td[1]')[0].text.strip()  # 注册资本
        except:
            business_term = '-'
        try:
            com_size = tree.xpath('//td[contains(text(),"人员规模") or contains(text(),"员工人数") or contains(text(),"律师人数") and @class="tb"]/following-sibling::td[1]')[0].text.strip()  # 人员规模
        except:
            com_size = '-'
        try:
            com_en_name = tree.xpath('//td[contains(text(),"英文名")]/following-sibling::td[1]')[0].text.strip()  # 英文名
        except:
            com_en_name = '-'
        if 'textShowMore' in res:
            intro = tree.xpath('string(//*[@id="textShowMore"])').replace('"', '·').strip()  # 介绍
        elif 'jianjieModal' in res and 'modal-dialog nmodal' in res:
            intro = tree.xpath('string(//*[@id="jianjieModal"]/div[@class="modal-dialog nmodal"]/div[@class="modal-content"]/div[@class="modal-body"])').replace('"', '·').strip()  # 介绍
        else:
            try:
                intro = tree.xpath('//td[contains(text(),"公司介绍：")]/following-sibling::td[1]|//td[contains(text(),"机构简介") and @class="tb"]/following-sibling::td[1]')[0].text.replace('"', '·').strip()  # 公司介绍
            except:
                intro = '-'

    def test_func(self):
        cm = ComBase()
        # url = 'https://www.qichacha.com/firm_4bc5df621fe97bb4ff722d9d041a475c.html' #中国科学院沈阳科学仪器股份有限公司
        url = 'https://www.qichacha.com/firm_h6d03b05405fe0a02a6c092382eee91e.html' #香港興業國際集團有限公司，香港公司
        # url = 'https://www.qichacha.com/firm_3f603703d59a04cbe427e5825099a565.html' #百度
        # url = 'https://www.qichacha.com/firm_c70a55cb048c8e4db7bca357a2c113e0.html' #阿里巴巴
        # url = 'https://www.qichacha.com/firm_gbfa3e0b8a8a13706d8269118c68a86c.html' #河南省烟草专卖驻郑州铁路局烟草专卖局
        header = cm.gh.header()
        res = requests.get(url,headers=header).text
        # print(res)
        tree = cm.gm.verify(res)
        return tree






if __name__ == '__main__':
    cm = ComBase()
    tree = cm.test_func()
    cm.verify_com_type(tree)

