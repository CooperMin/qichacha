#! /usr/bin/env python3
# -*- coding:utf-8 -*-
"""
企查查-信用信息-被执行人
"""
import time
import random
import requests

from lxml import etree

from support.mysql import QccMysql as db
from support.others import TimeInfo as tm
from support.others import DealKey as dk
from support.headers import GeneralHeaders as gh

class Credit():
    def get_com_id(self): #随机获取一条符合条件的公司信息
        sel = """
        SELECT `com_id`,`com_name`
        FROM `com_info`
        WHERE `origin`
        IS NOT NULL AND LENGTH(`com_id`) > 5 AND `status_credit_execued` IS NULL
        ORDER BY RAND() LIMIT 1;
        """

        # 测试sql#
        # sel = """
        # SELECT `com_id`, `com_name`
        # FROM `com_info`
        # WHERE com_id = '299eee201318f0283f086b4847d69fc7';
        # """
        # 测试sql#

        result = db().selsts(sel)
        if result == ():
            result = [None,None]
        else:
            result = result[0]
        return result

    def upd_status_execued(self,com_id,count): #更新com_info表相关字段状态码
        if count == -1:
            status = -1
        elif count == 0:
            status = 0
        else:
            status = 9
        upd = f"""
        UPDATE 
        `com_info` 
        SET
        `status_credit_execued` = "{status}",`count_credit_execued` = "{count}"
        WHERE 
        `com_id` = "{com_id}" ;
        """
        db().updsts(upd)

    def execued_judge(self): #判断执行人信息，如果有记录则执行解析，返回该公司相关信息
        global com_id,com_name
        cd = Credit()
        count_execued = 0
        count = 0
        while count_execued == 0 or count_execued == -1:
            result = cd.get_com_id()
            com_id = result[0]
            com_name = result[1]
            if com_id == None:
                pass
            else:
                count += 1
                com_url = f'https://www.qichacha.com/firm_{com_id}.html'
                hds = gh().header()
                time.sleep(random.randint(3,5))
                res = requests.get(com_url, headers=hds).text
                if '<script>window.location.href' in res:
                    print('访问频繁，需验证！{execued_judge}')
                    input('暂停')
                elif '<script>location.href="/user_login"</script>' in res:
                    print('Cookie失效，需更换！{execued_judge}')
                    input('程序暂停运行！')
                elif '您的账号访问超频，请稍后访问或联系客服人员' in res:
                    print('账号访问超频，请更换账号！{execued_judge}')
                    input('程序暂停运行！')
                else:
                    tree = etree.HTML(res)
                    try:
                        count_execued = tree.xpath(f'//div[@class="company-nav-items"]/span[contains(text(),"被执行人")]/span/text()|//div[@class="company-nav-items"]/a[@data-pos="zhixinglist"]/span/text()')[0]
                        count_execued = int(count_execued)
                    except:
                        count_execued = -1
                    localtime = tm().get_localtime()  # 当前时间
                    print(localtime)
                    if count_execued == 0 or count_execued == -1:
                        print(f'计数器：{count}\n公司ID:{com_id}\n被执行人信息条数：无')
                    else:
                        print(f'计数器：{count}\n公司ID:{com_id}\n被执行人信息条数：{count_execued}')
                    cd.upd_status_execued(com_id,count_execued)
        return com_id,com_name,count_execued

    def get_page_count(self): #获取页码长度
        cd = Credit()
        result = cd.execued_judge()
        com_id = result[0]
        com_name = result[1]
        count_record = result[2]
        # print(f'count_record:{count_record}')
        if count_record % 10 == 0:
            count_page = count_record // 10
        else:
            count_page = count_record // 10 + 1
        value = [com_id,com_name,count_page,count_record]
        return value

    def get_page_info(self): #解析页面内容
        cd = Credit()
        value = cd.get_page_count()
        com_id = value[0]
        com_name = value[1]
        count_page = value[2]
        count_record = value[3]
        key = dk().search_key(com_name)
        count = 0
        for page in range(1,count_page+1):
            index_url = 'https://www.qichacha.com'
            page_url = f'{index_url}/company_getinfos?unique={com_id}&companyname={com_name}&p={page}&tab=susong&box=zhixing'
            hds = gh().header()
            hds.update({'Referer': f'{index_url}/firm_{com_id}.html'})
            time.sleep(random.randint(1, 2))
            res_pg = requests.get(page_url, headers=hds).text
            if '<script>window.location.href' in res_pg:
                print('访问频繁，需验证！{get_page_info}')
                input('暂停')
            elif '<script>location.href="/user_login"</script>' in res_pg:
                print('Cookie失效，需更换！{get_page_info}')
                input('程序暂停运行！')
            elif '您的账号访问超频，请稍后访问或联系客服人员' in res_pg:
                print('账号访问超频，请更换账号！{get_page_info}')
                input('程序暂停运行！')
            else:
                tree_pg = etree.HTML(res_pg)
                content_li = tree_pg.xpath('//table[@class="ntable ntable-odd"]/tr[position()>2]')
                for nbr,content in enumerate(content_li,1):
                    count += 1
                    try:
                        exec_num = content.xpath('td[1]/text()')[0]
                        case_num = content.xpath('td[2]/a/text()')[0]
                        case_id = content.xpath('td[2]/a[contains(@onclick,"showRelatModal")]/@onclick')[0].split('zhixing",')[1].split('"')[1]
                        case_url= 'id='.join(('https://www.qichacha.com/company_zhixingRelat?',case_id))
                        filing_time = content.xpath('td[3]/text()')[0]
                        court_of_exec = content.xpath('td[4]/text()')[0]
                        exec_obj = content.xpath('td[5]/text()')[0]
                        time.sleep(random.randint(1, 2))
                        res_info = requests.get(case_url, headers=hds).text
                        if '<script>window.location.href' in res_info:
                            print('访问频繁，需验证！{get_page_info}')
                            input('暂停')
                        elif '<script>location.href="/user_login"</script>' in res_info:
                            print('Cookie失效，需更换！{get_page_info}')
                            input('程序暂停运行！')
                        elif '您的账号访问超频，请稍后访问或联系客服人员' in res_info:
                            print('账号访问超频，请更换账号！{get_page_info}')
                            input('程序暂停运行！')
                        else:
                            tree_info = etree.HTML(res_info)
                            exec_person = tree_info.xpath('//table/tbody/tr[1]/td[2]/text()')[0]
                            occ = tree_info.xpath('//table/tbody/tr[1]/td[4]/text()')[0]
                    except:
                        exec_num = None
                        case_num = None
                        case_id = None
                        case_url = None
                        filing_time = None
                        court_of_exec = None
                        exec_obj = None
                        exec_person = None
                        occ = None
                    print('\n{0}--总第{1}条----{2}/{3}页--{0}\n'.format('-' * 9, count, page, count_page))
                    localtime = tm().get_localtime()  # 当前时间
                    create_time = localtime
                    print(f'当前时间：{create_time}')
                    print(f'公司ID：{com_id}\n序号:{exec_num}\n案号:{case_num}\n案例ID:{case_id}\n案例链接:{case_url}\n'
                          f'立案时间:{filing_time}\n执行法院:{court_of_exec}\n执行标的:{exec_obj}\n被执行人:{exec_person}\n身份证号/组织机构代码:{occ}\n')
                    if exec_num == None:
                        ins = """
                        INSERT INTO
                        `com_credit_execued`
                        (`com_id`,`exec_num`,`case_num`,`case_id`,`filing_time`,
                        `court_of_exec`,`exec_obj`,`exec_person`,`occ`,`create_time`)
                        VALUES
                        (NULL,NULL,NULL,NULL,NULL,
                        NULL,NULL,NULL,NULL);
                        """
                    else:
                        ins = f"""
                        INSERT INTO 
                        `com_credit_execued`
                        (`com_id`,`exec_num`,`case_num`,`case_id`,`filing_time`,
                        `court_of_exec`,`exec_obj`,`exec_person`,`occ`,`create_time`)
                        VALUES 
                        ("{com_id}","{exec_num}","{case_num}","{case_id}","{filing_time}",
                        "{court_of_exec}","{exec_obj}","{exec_person}","{occ}","{create_time}");
                        """
                    db().inssts(ins)

                    upd = f"""
                    UPDATE 
                    `com_info` 
                    SET
                    `status_credit_execued` = 1
                    WHERE 
                    `com_id` = "{com_id}" ;
                    """
                    db().updsts(upd)














if __name__ == '__main__':
    cd = Credit()
    while 1 == 1:
        print('Loading......\n')
        time.sleep(5)
        print('开始新一轮采集')
        cd.get_page_info()

