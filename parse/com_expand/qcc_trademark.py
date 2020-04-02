#! /usr/bin/env python3
# -*- coding:utf-8 -*-


import re
import time
import random
import requests
from lxml import etree
from urllib.parse import quote

from support.use_mysql import ConnMysql as db
from support.others import DealKey as dk
from support.others import TimeInfo as tm
from support.headers import GeneralHeaders as gh

class TradeMarkInfo():
    def __init__(self):
        self.db = db()
        self.dk = dk()
        self.gh = gh()

    def get_com_id(self):
        # sel = """
        # SELECT `com_id`,`com_name`,`status_tm`,`count_tm`
        # FROM `com_info`
        # WHERE `origin`
        # IS NOT NULL AND LENGTH(`com_id`) = 32
        # AND `status_tm` IS NULL
        # AND `count_patent` != '0'
        # ORDER BY RAND() LIMIT 1;
        # """
        # sel = """
        # SELECT b.`com_id`,b.`com_name`,b.`status_tm`,b.`count_tm`
        # FROM temp_ppp a JOIN com_info b
        # ON a.`com_name`=b.`com_name`
        # AND LENGTH(b.com_id)=32
        # AND b.`status_tm` IS NULL
        # AND count_tm != 0
        # ORDER BY RAND() LIMIT 1;
        # """
        sel = """
        SELECT `com_id`,`com_name`,`status_tm`,`count_tm`
        FROM `com_info`
        WHERE `other_id` LIKE '%ls1000%'
        AND LENGTH(`com_id`) = 32
        AND `status_tm` IS NULL
        AND `count_tm` != '0'
        ORDER BY RAND() LIMIT 1;
        """
        result = db().selsts(sel)
        if result == ():
            result = [None,None,None,None]
        else:
            result = result[0]
        return result

    def get_page_count(self): #获取页面页数
        tmi = TradeMarkInfo()
        result = tmi.get_com_id()
        com_id = result[0]
        com_name = result[1]

        # com_id = 'dfdc316cf68eb1c07ed298f85587232b' #测试代码，采集时需注释掉
        # com_name = '青岛极地海洋世界有限公司' #测试代码，采集时需注释掉
        key = tmi.dk.search_key(com_name)
        status = result[2]
        if com_id == None:
            value = [None,None,None]
        else:
            index_url = 'https://www.qcc.com'
            com_url = f'{index_url}/company_getinfos?unique={com_id}&companyname={key}&tab=assets'
            hds = tmi.gh.header()
            hds.update({'Referer': f'{index_url}/firm_{com_id}.html'})
            time.sleep(random.randint(1,2))
            res = requests.get(com_url,headers=hds).text
            tree = etree.HTML(res)
            count_trademark = tree.xpath('//span[@class="tbadge"]/text()')[0].strip()
            if count_trademark == '5000+':
                count_page = 500
            else:
                count_trademark = int(count_trademark)
                if count_trademark%10 == 0:
                    count_page = count_trademark//10
                else:
                    count_page = count_trademark//10 + 1
            value = [com_id,com_name,count_page,index_url]
        return value

    def get_page_info(self): #获取页面详情
        tmi = TradeMarkInfo()
        value = tmi.get_page_count()
        com_id = value[0]
        com_name = value[1]
        count_page = value[2]
        if com_id == None:
            pass
        else:
            key = tmi.dk.search_key(com_name)
            index_url = value[3]
            count = 0
            for page in range(1, count_page + 1):
                # 'https://www.qichacha.com/company_getinfos?unique=&companyname=&p=2&tab=assets&box=zhuanli&zlpublicationyear=&zlipclist=&zlkindcode=&zllegalstatus='
                page_url = f'{index_url}/company_getinfos?unique={com_id}&companyname={key}&p={page}&tab=assets&box=shangbiao'
                hds = tmi.gh.header()
                hds.update({'Referer': f'{index_url}/firm_{com_id}.html'})
                time.sleep(random.randint(1,2))
                res_tmi = requests.get(page_url, headers=hds).text
                tree_tmi = etree.HTML(res_tmi)
                content_li = tree_tmi.xpath('//table/tr[position()>1]')
                for content in content_li:
                    count += 1
                    tm_num = content.xpath('td[1]/text()')[0]
                    tm_logo_url = content.xpath('td[2]/img/@src')[0]
                    tm_name = content.xpath('td[3]/text()')[0]
                    tm_status = content.xpath('td[4]/text()')[0]
                    app_date = content.xpath('td[5]/text()')[0]
                    tm_regno = content.xpath('td[6]/text()')[0]
                    tm_int_type = content.xpath('td[7]/text()')[0]
                    trademark_link = content.xpath('td[8]/a/@href')[0]
                    trademark_url = ''.join((index_url,trademark_link))
                    time.sleep(random.randint(1,3))
                    res_dt = requests.get(trademark_url,headers=hds).text
                    tree_dt = etree.HTML(res_dt)
                    sim_groups = tree_dt.xpath('//table[@class="ntable"]/tbody/tr/td[contains(text(),"类似群")]/following-sibling::td[1]/text()')[0].strip()
                    app_cn = tree_dt.xpath('//table[@class="ntable"]/tbody/tr/td[contains(text(),"申请人名称（中文）")]/following-sibling::td[1]/text()')[0].strip()
                    app_en = tree_dt.xpath('//table[@class="ntable"]/tbody/tr/td[contains(text(),"申请人名称（英文）")]/following-sibling::td[1]/text()')[0].strip()
                    app_addr_cn = tree_dt.xpath('//table[@class="ntable"]/tbody/tr/td[contains(text(),"申请人地址（中文）")]/following-sibling::td[1]/text()')[0].strip()
                    app_addr_en = tree_dt.xpath('//table[@class="ntable"]/tbody/tr/td[contains(text(),"申请人地址（英文）")]/following-sibling::td[1]/text()')[0].strip()
                    first_trial_no = tree_dt.xpath('//table[@class="ntable"]/tbody/tr/td[contains(text(),"初审公告期号")]/following-sibling::td[1]/text()')[0].strip()
                    first_trial_date = tree_dt.xpath('//table[@class="ntable"]/tbody/tr/td[contains(text(),"初审公告日期")]/following-sibling::td[1]/text()')[0].strip().replace(' ','').replace('\n','')
                    reg_not_peri_no = tree_dt.xpath('//table[@class="ntable"]/tbody/tr/td[contains(text(),"注册公告期号")]/following-sibling::td[1]/text()')[0].strip()
                    reg_not_peri_date = tree_dt.xpath('//table[@class="ntable"]/tbody/tr/td[contains(text(),"注册公告日期")]/following-sibling::td[1]/text()')[0].strip()
                    is_comm_tm = tree_dt.xpath('//table[@class="ntable"]/tbody/tr/td[contains(text(),"是否共有商标")]/following-sibling::td[1]/text()')[0].strip()
                    tm_type = tree_dt.xpath('//table[@class="ntable"]/tbody/tr/td[contains(text(),"商标类型")]/following-sibling::td[1]/text()')[0].strip()
                    exclu_right_limit = tree_dt.xpath('//table[@class="ntable"]/tbody/tr/td[contains(text(),"专用权期限")]/following-sibling::td[1]/text()')[0].strip()
                    tm_form = tree_dt.xpath('//table[@class="ntable"]/tbody/tr/td[contains(text(),"商标形式")]/following-sibling::td[1]/text()')[0].strip()
                    int_reg_date = tree_dt.xpath('//table[@class="ntable"]/tbody/tr/td[contains(text(),"国际注册日期")]/following-sibling::td[1]/text()')[0].strip()
                    later_scheduled_date = tree_dt.xpath('//table[@class="ntable"]/tbody/tr/td[contains(text(),"后期指定日期")]/following-sibling::td[1]/text()')[0].strip()
                    prio_date = tree_dt.xpath('//table[@class="ntable"]/tbody/tr/td[contains(text(),"优先权日期")]/following-sibling::td[1]/text()')[0].strip()
                    try:
                        agency = tree_dt.xpath('//table[@class="ntable"]/tbody/tr/td[contains(text(),"代理/办理机构")]/following-sibling::td[1]/a/text()')[0].strip()
                    except:
                        agency = tree_dt.xpath('//table[@class="ntable"]/tbody/tr/td[contains(text(),"代理/办理机构")]/following-sibling::td[1]/text()')[0].strip()
                    service = tree_dt.xpath('//table[@class="ntable"]/tbody/tr/td[contains(text(),"商品/服务")]/following-sibling::td[1]/text()')[0].strip()
                    print('\n{0}--总第{1}条----{2}/{3}页--{0}\n'.format('-' * 9, count,page,count_page))
                    localtime = tm().get_localtime()  # 当前时间
                    create_time = localtime
                    print(f'当前时间：{localtime}')
                    print(f'公司ID:{com_id}\n公司名称:{com_name}')
                    print(f'序号:{tm_num}\n商标LOGO URL:{tm_logo_url}\n商标名称:{tm_name}\n商标状态:{tm_status}\n申请时间:{app_date}\n'
                          f'申请/注册号:{tm_regno}\n国际类型:{tm_int_type}\n类似群:{sim_groups}\n申请人名称（中文）:{app_cn}\n申请人名称（英文）:{app_en}\n'
                          f'申请人地址（中文）:{app_addr_cn}\n申请人地址（英文）:{app_addr_en}\n初审公告期号:{first_trial_no}\n初审公告日期:{first_trial_date}\n注册公告期号:{reg_not_peri_no}\n'
                          f'注册公告日期:{reg_not_peri_date}\n是否共有商标:{is_comm_tm}\n商标类型:{tm_type}\n专用权期限:{exclu_right_limit}\n商标形式:{tm_form}\n'
                          f'国际注册日期:{int_reg_date}\n后期指定日期:{later_scheduled_date}\n优先权日期:{prio_date}\n代理机构:{agency}\n商品/服务:{service}')
                    ins = f"""
                    INSERT INTO  
                    `com_trademark`
                    (`com_id`,`tm_num`,`tm_logo_url`,`tm_name`,`tm_status`,
                    `app_date`,`tm_regno`,`tm_int_type`,`sim_groups`,`app_cn`,
                    `app_en`,`app_addr_cn`,`app_addr_en`,`first_trial_no`,`first_trial_date`,
                    `reg_not_peri_no`,`reg_not_peri_date`,`is_comm_tm`,`tm_type`,`exclu_right_limit`,
                    `tm_form`,`int_reg_date`,`later_scheduled_date`,`prio_date`,`agency`,
                    `service`,`create_time`)
                    VALUES 
                    ("{com_id}","{tm_num}","{tm_logo_url}","{tm_name}","{tm_status}",
                    "{app_date}","{tm_regno}","{tm_int_type}","{sim_groups}","{app_cn}",
                    "{app_en}","{app_addr_cn}","{app_addr_en}","{first_trial_no}","{first_trial_date}",
                    "{reg_not_peri_no}","{reg_not_peri_date}","{is_comm_tm}","{tm_type}","{exclu_right_limit}",
                    "{tm_form}","{int_reg_date}","{later_scheduled_date}","{prio_date}","{agency}",
                    "{service}","{create_time}");
                    """
                    db().inssts(ins)

                    upd = f"""
                    UPDATE 
                    `com_info` 
                    SET
                    `status_tm` = 1
                    WHERE 
                    `com_id` = "{com_id}" ;
                    """
                    db().updsts(upd)
                    # input('暂停')
            localtime = tm().get_localtime()  # 当前时间
            print('\n{1}\n{0}数据采集完成!{0}\n{1}'.format('+' * 7, '+' * 25))
            print(f'当前时间：{localtime}')





if __name__ == '__main__':
    tmi = TradeMarkInfo()
    # pt.get_com_id()
    while 1 == 1:
        time.sleep(3)
        print('开始新一轮采集')
        tmi.get_page_info()

    # PatentInfo().getinfo()