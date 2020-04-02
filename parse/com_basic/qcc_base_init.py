#! /usr/bin/env python3
import os
import re
import time
import requests
from urllib.parse import quote

from support.use_mysql import ConnMysql as db
from support.others import DealKey as dk
from support.others import TimeInfo as tm
from support.headers import GeneralHeaders as gh
from parse.com_common.common import GeneralMethod as gm
from parse.com_basic.qcc_base_parse import BaseInfoParse as bip
from parse.com_basic.qcc_base_sql import ins_tb_com as itc

INS_TB = 0
UPD_TB = 1


def get_com_list_from_file():  # 读取文件，获取公司列表
    com_file = os.path.abspath(os.path.join(os.getcwd(), '../../doc/company_list'))
    with open(com_file, 'r', encoding='utf-8') as rf:
        rf = rf.readlines()
    com_list = []
    for company in rf:
        company = company.strip()
        com_list.append(company)
    return com_list


def input_sql():
    sql = """
         SELECT com_name 
         FROM com_info 
         WHERE  LENGTH(com_id)=32
         AND `chain` IS NOT NULL
         LIMIT 10;
        """
    return sql


def verify_result_is_not_null():
    pass


class ComBase:
    def __init__(self):
        self.db = db()
        self.dk = dk()
        self.gh = gh()
        self.gm = gm()
        self.tm = tm()

    def get_com_list_from_db(self, sq):
        try:
            com_tup = self.db.selsts(sq)
            com_list = []
            for company in com_tup:
                com_list.append(company[0])
            return com_list
        except:
            sel = None
            return print('未查询到企业信息！')

    def com_search(self, com_name):  # 根据关键词/公司名称检索匹配最优公司
        header = self.gh.header()
        parm = self.dk.search_key(com_name)
        url_search = f'https://www.qichacha.com/search?key={parm}'
        res = requests.get(url_search, headers=header).text
        self.tm.random_sec()
        tree = self.gm.verify(res)
        num = int(tree.xpath('//span[@id="countOld"]/span[1]/text()')[0].strip())
        kw = com_name.replace('（', '(').replace('）', ')')
        if tree is None or num == 0:
            com_id = None
            com_url = None
            print(f'未检索到公司名称类似 {kw} 的相关企业！')
        else:
            index_url = 'https://www.qcc.com'
            try:
                # 获取检索结果，匹配与所给公司名称最接近的公司的链接
                com_link = tree.xpath('//*[@id="search-result"]/tr[1]/td[2]/a[@class="ma_h1"]/@href')[0]
            except:
                # 获取检索结果，匹配与所给公司名称最接近的公司的链接
                com_link = tree.xpath('//*[@id="search-result"]/tr[1]/td[3]/a[@class="ma_h1"]/@href')[0]
                if 'groupdetail' in com_link:
                    try:
                        com_link = tree.xpath('//*[@id="search-result"]/tr[2]/td[2]/a[@class="ma_h1"]/@href')[0]
                    except:
                        com_link = tree.xpath('//*[@id="search-result"]/tr[2]/td[3]/a[@class="ma_h1"]/@href')[0]
            com_id = re.findall(r'(?<=/firm_)(.*)(?=\.html)', com_link)[0]
            com_url = ''.join((index_url, com_link))  # 拼接为完整链接)
        return com_id, kw, com_url, url_search

    def req_com_page(self, com_id, kw, com_url, url_search): #返回公司信息页源码
        header = self.gh.header()
        header.update({'Referer':f'{url_search}'})
        res = requests.get(com_url, headers=header).text
        time.sleep(self.tm.random_sec())
        tree = self.gm.verify(res)
        return tree, com_id, kw

    def req_com_other_page(self, com_id, com_url):
        header = self.gh.header()
        header.update({'Referer': f'https://www.qcc.com/firm_{com_id}.shtml',
                       'X-Requested-With': 'XMLHttpRequest'})
        res = requests.get(com_url, headers=header).text
        self.tm.random_sec()
        tree = self.gm.verify(res)
        return tree

    def excu_com(self, com_list):
        if com_list is not None:
            company_count = len(com_list)
            print('数据采集中...')
            for num,company_name in enumerate(com_list,1):
                # for company_name in com_list:
                # company_name = '青岛恒星科技学院'
                # company_name = '央视动漫集团有限公司'
                # company_name = '阿里巴巴（中国）网络技术有限公司'
                # company_name = '阿里巴巴文化娱乐有限公司'
                # company_name = '招商银行股份有限公司'
                # company_name = '中国人寿保险股份有限公司'
                # company_name = '深圳市亿道控股集团'
                # company_name = '延安八九八商品交易中心有限公司'
                # company_name = '青岛兮易信息技术有限公司'
                # company_name = '南順（香港）有限公司'
                # company_name = '臺灣華培企業有限公司'
                # company_name = '郑州大学'
                # company_name = '郑州大学校友会'
                # company_name = '郑州大学教育发展基金会'
                # company_name = '湖南君富律师事务所'

                value = self.com_search(company_name)
                com_id = value[0]
                kw = value[1]
                com_url = value[2]
                url_search = value[3]
                if com_id is None:
                    print('无此公司信息')
                    un_search_file = os.path.abspath(os.path.join(os.getcwd(), '../../doc/un_search.txt'))
                    with open(un_search_file, 'a+', encoding='utf-8') as wf:
                        wf.writelines(f'{company_name}\n')
                    """
                    诸如将未检索到的企业信息打印输出日志等
                    ...其它操作
                    """
                    pass
                else:
                    out_come = self.req_com_page(com_id, kw, com_url, url_search)
                    tree = out_come[0]
                    com_id = out_come[1]
                    kw = out_come[2]
                    com_name = tree.xpath('//input[@name="toCompanyName"]/@value')[0].strip().replace('（', '(').replace('）', ')')
                    parm = self.dk.search_key(com_name)
                    com_url = f'https://www.qcc.com/company_getinfos?unique={com_id}&companyname={quote(parm)}&tab=base'
                    result = bip(tree).verify_is_listed()
                    basic = bip(tree).common_word()
                    ori_type = bip(tree).verify_ori_type()
                    new_tree = self.req_com_other_page(com_id, com_url)
                    if ori_type == '大陆企业':
                        bip(tree).land_com(result, basic, ori_type, com_id, kw, num, company_count)
                        # arg = bip(tree).land_com(result, basic, ori_type, com_id, kw)
                        # itc(arg).ins_land_com()
                    elif ori_type == '香港企业' or ori_type == '未被标记的港澳企业':
                        bip(new_tree).hk_com(result, basic, ori_type, com_id, kw, num, company_count)
                    elif ori_type == '台湾企业':
                        bip(new_tree).tw_com(result, basic, ori_type, com_id, kw, num, company_count)
                    elif ori_type == '社会组织':
                        bip(new_tree).social_ori(basic, ori_type, com_id, kw, num, company_count)
                    elif ori_type == '基金会':
                        bip(tree).foundation(basic, ori_type, com_id, kw, num, company_count)
                    elif ori_type == '事业单位':
                        bip(tree).public_institution(basic, ori_type, com_id, kw, num, company_count)
                    elif ori_type == '学校':
                        bip(tree).public_institution(basic, ori_type, com_id, kw, num, company_count)
                    elif ori_type == '医院':
                        bip(tree).public_institution(basic, ori_type, com_id, kw, num, company_count)
                    elif ori_type == '律所':
                        bip(tree).law_firm(basic, ori_type, com_id, kw, num, company_count)
                    else:
                        ori_type = '未被标记的企事业单位/律所'
                        bip(tree).public_institution(basic, ori_type, com_id, kw, num, company_count)
            print('采集完成!')
        else:
            exit(print('不符合当前的采集要求!'))

    def running(self):
        cba = ComBase()
        com_list = get_com_list_from_file()
        cba.excu_com(com_list)











if __name__ == '__main__':
    cba = ComBase()
    # 从文件中读取方式获取待采集的公司列表
    # com_list = get_com_list_from_file()
    # 从数据库中读取方式获取待采集的公司列表
    # sql = input_sql()
    # com_list = cba.get_com_list_from_db(sql)
    # cba.excu_com(com_list)
    cba.running()

