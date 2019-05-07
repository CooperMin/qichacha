#! /usr/bin/env python3
# -*- coding:utf-8 -*-


import re
import time
import random
import requests
from lxml import etree
from urllib.parse import quote

from support.mysql import QccMysql as db
from support.others import timeInfo as tm
from support.headers import GeneralHeaders as gh

class PatentInfo():

    def get_com_id(self):
        sel = """
        SELECT `com_id`,`com_name`,`status_patent`,`count_patent`
        FROM `com_info` 
        WHERE `origin` 
        IS NOT NULL AND LENGTH(`com_id`) > 5 AND `status_patent` IS NULL AND `count_patent` != '0'
        ORDER BY RAND() LIMIT 1;
        """
        result = db().selsts(sel)
        if result == ():
            result = [None,None,None,None]
        else:
            result = result[0]
        return result

    def search_key(self,key): #根据关键词进行检索
        zh_model = re.compile(u'[\u4e00-\u9fa5]')
        match = zh_model.search(key)
        if match: #判断是否包含汉字，如果包含则对汉字做处理
            key = quote(key)
        return key

    def get_page_count(self): #获取页面页数
        pt = PatentInfo()
        result = pt.get_com_id()
        com_id = result[0]
        com_name = result[1]

        # com_id = '608886557bb9cf989ae600d1e8a94d40' #测试代码，采集时需注释掉
        # com_name = '网易(杭州)网络有限公司' #测试代码，采集时需注释掉
        key = pt.search_key(com_name)
        status = result[2]
        if com_id == None:
            value = [None,None,None]
        else:
            index_url = 'https://www.qichacha.com'
            com_url = f'{index_url}/company_getinfos?unique={com_id}&companyname={key}&tab=assets'
            hds = gh().header()
            hds.update({'Referer': f'{index_url}/firm_{com_id}.html'})
            time.sleep(random.randint(1,2))
            res = requests.get(com_url,headers=hds).text
            tree = etree.HTML(res)

            count_patent = tree.xpath('//*[contains(text(),"专利信息") and @class="title"]/following-sibling::span[@class="tbadge"]/text()')[0].strip()
            if count_patent == '5000+':
                count_page = 500
            else:
                count_patent = int(count_patent)
                if count_patent%10 == 0:
                    count_page = count_patent//10
                else:
                    count_page = count_patent//10 + 1
            value = [com_id,com_name,count_page,index_url]
        return value

    def get_page_info(self): #获取页面详情
        pt = PatentInfo()
        value = pt.get_page_count()
        com_id = value[0]
        com_name = value[1]
        count_page = value[2]

        # 临时代码，供单次补采数据【001】
        com_id = '1ad3c9eea1707efaaf2647126b968c78'
        com_name = '珠海市魅族科技有限公司'
        count_page = 390
        # 临时代码，供单次补采数据【001】

        if com_id == None:
            pass
        else:
            key = pt.search_key(com_name)
            index_url = value[3]
            count = 0
            for page in range(339, count_page + 1): #临时代码，供单次补采数据【001】
            # for page in range(1, count_page + 1):
                page_url = f'{index_url}/company_getinfos?unique={com_id}&companyname={key}&p={page}&tab=assets&box=zhuanli'
                hds = gh().header()
                hds.update({'Referer': f'{index_url}/firm_{com_id}.html'})
                time.sleep(random.randint(1,2))
                res_pg = requests.get(page_url, headers=hds).text
                tree_pg = etree.HTML(res_pg)
                content_li = tree_pg.xpath('//table/tr[position()>1]')
                for content in content_li:
                    count += 1
                    patent_num = content.xpath('td[1]/text()')[0]
                    patent_type = content.xpath('td[2]/text()')[0]
                    patent_pub_num = content.xpath('td[3]/text()')[0]
                    patent_pub_date = content.xpath('td[4]/text()')[0]
                    patent_name = content.xpath('td[5]/a/text()')[0].strip()
                    patent_link = content.xpath('td[5]/a/@href')[0]
                    patent_url = ''.join((index_url,patent_link))
                    time.sleep(random.randint(1,3))
                    res_dt = requests.get(patent_url,headers=hds).text
                    tree_dt = etree.HTML(res_dt)
                    app_num = tree_dt.xpath('//table[@class="ntable"]/tbody/tr/td[contains(text(),"申请号")]/following-sibling::td[1]/text()')[0].strip()
                    app_date = tree_dt.xpath('//table[@class="ntable"]/tbody/tr/td[contains(text(),"申请日")]/following-sibling::td[1]/text()')[0].strip()
                    prio_date = tree_dt.xpath('//table[@class="ntable"]/tbody/tr/td[contains(text(),"优先权日")]/following-sibling::td[1]/text()')[0].strip()
                    prio_num = tree_dt.xpath('//table[@class="ntable"]/tbody/tr/td[contains(text(),"优先权号")]/following-sibling::td[1]/text()')[0].strip()
                    inventor = tree_dt.xpath('//table[@class="ntable"]/tbody/tr/td[contains(text(),"发明人")]/following-sibling::td[1]/text()')[0].strip()
                    try:
                        applicant = tree_dt.xpath('//table[@class="ntable"]/tbody/tr/td[contains(text(),"申请（专利权）人")]/following-sibling::td[1]/a/text()')[0].strip()
                    except:
                        applicant = tree_dt.xpath('//table[@class="ntable"]/tbody/tr/td[contains(text(),"申请（专利权）人")]/following-sibling::td[1]')[0].strip()
                    try:
                        agency = tree_dt.xpath('//table[@class="ntable"]/tbody/tr/td[contains(text(),"代理机构")]/following-sibling::td[1]/a/text()')[0].strip()
                    except:
                        agency = tree_dt.xpath('//table[@class="ntable"]/tbody/tr/td[contains(text(),"代理机构")]/following-sibling::td[1]/text()')[0].strip()
                    agent = tree_dt.xpath('//table[@class="ntable"]/tbody/tr/td[contains(text(),"代理人")]/following-sibling::td[1]/text()')[0].strip()
                    ipc = tree_dt.xpath('//table[@class="ntable"]/tbody/tr/td[contains(text(),"IPC分类号")]/following-sibling::td[1]/text()')[0].strip().replace(' ','').replace('\n','')
                    cpc = tree_dt.xpath('//table[@class="ntable"]/tbody/tr/td[contains(text(),"CPC分类号")]/following-sibling::td[1]/text()')[0].strip()
                    app_address = tree_dt.xpath('//table[@class="ntable"]/tbody/tr/td[contains(text(),"申请人地址")]/following-sibling::td[1]/text()')[0].strip()
                    app_zip_code = tree_dt.xpath('//table[@class="ntable"]/tbody/tr/td[contains(text(),"申请人邮编")]/following-sibling::td[1]/text()')[0].strip()
                    abstract = tree_dt.xpath('//table[@class="ntable"]/tbody/tr/td[contains(text(),"摘要")]/following-sibling::td[1]/text()')[0].strip()
                    try:
                        abstract_photo = tree_dt.xpath('//table[@class="ntable"]/tbody/tr/td[contains(text(),"摘要附图")]/following-sibling::td[1]/img/@src')[0].strip()
                    except:
                        abstract_photo = '-'
                    try:
                        claim = tree_dt.xpath('//table[@class="ntable"]/tr/td[@class="ea_instructions" and position()=1]/p/text()')
                        claim = ''.join(claim)
                    except:
                        claim = '-'
                    try:
                        instructions = tree_dt.xpath('//div[@class="tcaption"]/h3[text()="说明书"]/parent::div/following-sibling::table[@class="ntable"]/tr/td[@class="ea_instructions"]/h1/text()|//div[@class="tcaption"]/h3[text()="说明书"]/parent::div/following-sibling::table[@class="ntable"]/tr/td[@class="ea_instructions"]/h2/text()|//div[@class="tcaption"]/h3[text()="说明书"]/parent::div/following-sibling::table[@class="ntable"]/tr/td[@class="ea_instructions"]/p/text()')
                        instructions = ''.join(instructions)
                    except:
                        instructions = '-'
                    print('\n{0}--总第{1}条----{2}/{3}页--{0}\n'.format('-' * 9, count,page,count_page))
                    localtime = tm().get_localtime()  # 当前时间
                    print(f'公司ID:{com_id} 当前时间：{localtime}')
                    print(f'序号:{patent_num}\n专利类型:{patent_type}\n公开（公告）号:{patent_pub_num}\n公开（公告）日期:{patent_pub_date}\n专利名称:{patent_name}\n'
                          f'专利页URL:{patent_url}\n申请号:{app_num}\n申请日期:{app_date}\n优先权日:{prio_date}\n优先权号:{prio_num}\n'
                          f'发明人:{inventor}\n申请（专利权）人:{applicant}\n代理机构:{agency}\n代理人:{agent}\nIPC分类号:{ipc}\n'
                          f'CPC分类号:{cpc}\n申请人地址:{app_address}\n申请人邮编:{app_zip_code}\n摘要:{abstract}\n摘要附图:{abstract_photo}\n'
                          f'权利要求:{claim}\n说明书:{instructions}')
                    ins = f"""
                    INSERT INTO  
                    `com_patent`
                    (`com_id`,`patent_num`,`patent_type`,`patent_pub_num`,`patent_pub_date`,
                    `patent_name`,`patent_url`,`app_num`,`app_date`,`prio_date`,
                    `prio_num`,`inventor`,`applicant`,`agency`,`agent`,
                    `ipc`,`cpc`,`app_address`,`app_zip_code`,`abstract`,`abstract_photo`,
                    `claim`,`instructions`)
                    VALUES 
                    ("{com_id}","{patent_num}","{patent_type}","{patent_pub_num}","{patent_pub_date}",
                    "{patent_name}","{patent_url}","{app_num}","{app_date}","{prio_date}",
                    "{prio_num}","{inventor}","{applicant}","{agency}","{agent}",
                    "{ipc}","{cpc}","{app_address}","{app_zip_code}","{abstract}","{abstract_photo}",
                    "{claim}","{instructions}");
                    """
                    db().inssts(ins)

                    upd = f"""
                    UPDATE 
                    `com_info` 
                    SET
                    `status_patent` = 1
                    WHERE 
                    `com_id` = "{com_id}" ;
                    """
                    db().updsts(upd)
            localtime = tm().get_localtime()  # 当前时间
            print('\n{1}\n{0}数据采集完成!{0}\n{1}'.format('+' * 7, '+' * 25))
            print(f'当前时间：{localtime}\n')
            time.sleep(3)





if __name__ == '__main__':
    pt = PatentInfo()
    # pt.get_com_id()
    while 1 == 1:
        print('Loading......')
        time.sleep(5)
        print('开始新一轮采集')
        pt.get_page_info()

    # PatentInfo().getinfo()