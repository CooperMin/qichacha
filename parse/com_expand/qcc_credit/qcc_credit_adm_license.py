#! /usr/bin/env python3
# -*- coding:utf-8 -*-
"""
企查查-行政许可[工商局]
"""
import json
import time
import random
import requests

from lxml import etree

from support.use_mysql import QccMysql as db
from support.others import DealKey as dk
from support.others import TimeInfo as tm
from support.headers import GeneralHeaders as gh

class AdmLicense():
    def get_com_id(self):  # 随机获取一条符合条件的公司信息
        sel = """
        SELECT `com_id`,`com_name`
        FROM `com_info`
        WHERE `origin`
        IS NOT NULL AND LENGTH(`com_id`) > 5 AND `status_credit_adm_license` IS NULL
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
            result = [None, None]
        else:
            result = result[0]
        return result

    def upd_status(self, com_id,status_column,count_column, count):  # 更新com_info表相关字段状态码
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
            `{status_column}` = "{status}",`{count_column}` = "{count}"
            WHERE 
            `com_id` = "{com_id}" ;
            """
        db().updsts(upd)

    def adm_license_judge(self):  # 判断行政许可信息，如果有记录则执行解析，返回该公司相关信息
        global com_id, com_name
        al = AdmLicense()
        count_adm_license = 0
        count = 0
        while count_adm_license == 0 or count_adm_license == -1:
            result = al.get_com_id()
            com_id = result[0]
            com_name = result[1]
            if com_id == None:
                pass
            else:
                count += 1
                com_url = f'https://www.qichacha.com/firm_{com_id}.html'
                hds = gh().header()
                time.sleep(random.randint(3, 5))
                res = requests.get(com_url, headers=hds).text
                if '<script>window.location.href' in res:
                    print('访问频繁，需验证！{adm_license_judge}')
                    input('暂停')
                elif '<script>location.href="/user_login"</script>' in res:
                    print('Cookie失效，需更换！{adm_license_judge}')
                    input('程序暂停运行！')
                elif '您的账号访问超频，请稍后访问或联系客服人员' in res:
                    print('账号访问超频，请更换账号！{adm_license_judge}')
                    input('程序暂停运行！')
                else:
                    tree = etree.HTML(res)
                    try:
                        count_adm_license = tree.xpath('//div[@class="company-nav-items"]/span[contains(text(),"行政许可")]/span/text()|//div[@class="company-nav-items"]/a[@data-pos="licenslist"]/span/text()')[0]
                        count_adm_license = int(count_adm_license)
                    except:
                        count_adm_license = -1
                    localtime = tm().get_localtime()  # 当前时间
                    print(localtime)
                    if count_adm_license == 0 or count_adm_license == -1:
                        print(f'计数器：{count}\n公司ID:{com_id}\n行政许可信息条数：无')
                    else:
                        print(f'计数器：{count}\n公司ID:{com_id}\n行政许可信息条数：{count_adm_license}')
                    status_column = 'status_credit_adm_license' #表字段名
                    count_column = 'count_credit_adm_license' #表字段名
                    al.upd_status(com_id,status_column,count_column,count_adm_license)
        return com_id, com_name, count_adm_license

class AdmLicenseBc(AdmLicense):
    def bc_judge(self):
        global com_id,com_name
        alb = AdmLicenseBc()
        count_bc = 0
        count = 0
        while count_bc == 0:
            result = alb.adm_license_judge()
            com_id = result[0]
            com_name = result[1]
            key = dk().search_key(com_name)
            if com_id == None:
                pass
            else:
                count += 1
                com_url = f'https://www.qichacha.com/firm_{com_id}.html'
                hds = gh().header()
                time.sleep(random.randint(3, 5))
                res = requests.get(com_url, headers=hds).text
                if '<script>window.location.href' in res:
                    print('访问频繁，需验证！{bc_judge}')
                    input('暂停')
                elif '<script>location.href="/user_login"</script>' in res:
                    print('Cookie失效，需更换！{bc_judge}')
                    input('程序暂停运行！')
                elif '您的账号访问超频，请稍后访问或联系客服人员' in res:
                    print('账号访问超频，请更换账号！{bc_judge}')
                    input('程序暂停运行！')
                else:
                    tree = etree.HTML(res)
                    try:
                        count_bc = tree.xpath('//div[@class="tcaption"]/h3[contains(text(),"[工商局]")]/following-sibling::span[1]/text()')[0]
                        count_bc = int(count_bc)
                    except:
                        count_bc = 0
                    localtime = tm().get_localtime()  # 当前时间
                    print(localtime)
                    if count_bc == 0:
                        print(f'计数器：{count}\n公司ID:{com_id}\n行政许可信息[工商局]条数：无')
                    else:
                        print(f'计数器：{count}\n公司ID:{com_id}\n行政许可信息[工商局]条数：{count_bc}')
                    status_column = 'status_credit_adm_license_bc'  # 表字段名
                    count_column = 'count_credit_adm_license_bc'  # 表字段名
                    alb.upd_status(com_id, status_column, count_column, count_bc)
        return com_id, com_name, count_bc

    def get_page_count(self):  # 获取页码长度
        alb = AdmLicenseBc()
        result = alb.bc_judge()
        com_id = result[0]
        com_name = result[1]
        count_record = result[2]
        if count_record % 10 == 0:
            count_page = count_record // 10
        else:
            count_page = count_record // 10 + 1
        value = [com_id, com_name, count_page, count_record]
        return value

    def get_page_info(self):  # 解析页面内容
        alb = AdmLicenseBc()
        value = alb.get_page_count()
        com_id = value[0]
        com_name = value[1]
        count_page = value[2]
        count_record = value[3]
        key = dk().search_key(com_name)
        count = 0
        for page in range(1, count_page + 1):
            index_url = 'https://www.qichacha.com'
            page_url = f'{index_url}/company_getinfos?unique={com_id}&companyname={key}&p={page}&tab=run&box=licens'
            hds = gh().header()
            hds.update({'Referer': f'{index_url}/firm_{com_id}.html'})
            time.sleep(random.randint(1, 2))
            res = requests.get(page_url, headers=hds).text
            if '<script>window.location.href' in res:
                print('访问频繁，需验证！{get_page_info[2]}')
                input('暂停')
            elif '<script>location.href="/user_login"</script>' in res:
                print('Cookie失效，需更换！{get_page_info[2]}')
                input('程序暂停运行！')
            elif '您的账号访问超频，请稍后访问或联系客服人员' in res:
                print('账号访问超频，请更换账号！{get_page_info[2]}')
                input('程序暂停运行！')
            else:
                tree = etree.HTML(res)
                content_li = tree.xpath('//table[@class="ntable ntable-odd"]/tr[position()>2]')
                for nbr, content in enumerate(content_li, 1):
                    count += 1
                    try:
                        license_num = content.xpath('td[1]/text()')[0]
                        license_doc_num = content.xpath('td[2]/text()')[0]
                        license_doc_name = content.xpath('td[3]/text()')[0]
                        valid_period_from = content.xpath('td[4]/text()')[0]
                        valid_period_to = content.xpath('td[5]/text()')[0]
                        license_office =  content.xpath('td[6]/text()')[0]
                        license_content = content.xpath('td[7]/text()')[0]
                    except:
                        license_num = None
                        license_doc_num = None
                        license_doc_name = None
                        valid_period_from = None
                        valid_period_to = None
                        license_office = None
                        license_content = None

                    print('\n{0}--总第{1}条----{2}/{3}页--{0}\n'.format('-' * 9, count, page, count_page))
                    localtime = tm().get_localtime()  # 当前时间
                    create_time = localtime
                    print(f'当前时间：{create_time}')
                    print(f'公司ID：{com_id}\n序号:{license_num}\n许可文件编号:{license_doc_num}\n许可文件名称:{license_doc_name}\n有效期自:{valid_period_from}\n'
                          f'有效期至:{valid_period_to}\n许可机关:{license_office}\n许可内容:{license_content}')
                    if license_num == None:
                        ins = """
                        INSERT INTO
                        `com_credit_adm_license_bc`
                        (`com_id`,`license_num`,`license_doc_num`,`license_doc_name`,`valid_period_from`,
                        `valid_period_to`,`license_office`,`license_content`,`create_time`)
                        VALUES
                        (NULL,NULL,NULL,NULL,NULL,
                        NULL,NULL,NULL,NULL);
                        """
                    else:
                        ins = f"""
                        INSERT INTO
                        `com_credit_adm_license_bc`
                        (`com_id`,`license_num`,`license_doc_num`,`license_doc_name`,`valid_period_from`,
                        `valid_period_to`,`license_office`,`license_content`,`create_time`)
                        VALUES
                        ("{com_id}","{license_num}","{license_doc_num}","{license_doc_name}","{valid_period_from}",
                        "{valid_period_to}","{license_office}","{license_content}","{create_time}");
                        """
                    db().inssts(ins)

                    upd = f"""
                        UPDATE 
                        `com_info` 
                        SET
                        `status_credit_adm_license_bc` = 1
                        WHERE 
                        `com_id` = "{com_id}" ;
                        """
                    db().updsts(upd)

        localtime = tm().get_localtime()  # 当前时间
        print('\n{1}\n{0}数据采集完成!{0}\n{1}'.format('+' * 7, '+' * 25))
        print(f'当前时间：{localtime}\n')
        time.sleep(3)

class AdmLicenseCc(AdmLicense): #行政许可[信用中国]
    def cc_judge(self):
        global com_id,com_name
        alb = AdmLicenseCc()
        count_cc = 0
        count = 0
        while count_cc == 0:
            result = alb.adm_license_judge()
            com_id = result[0]
            com_name = result[1]
            key = dk().search_key(com_name)
            if com_id == None:
                pass
            else:
                count += 1
                com_url = f'https://www.qichacha.com/firm_{com_id}.html'
                hds = gh().header()
                time.sleep(random.randint(3, 5))
                res = requests.get(com_url, headers=hds).text
                if '<script>window.location.href' in res:
                    print('访问频繁，需验证！{cc_judge}')
                    input('暂停')
                elif '<script>location.href="/user_login"</script>' in res:
                    print('Cookie失效，需更换！{cc_judge}')
                    input('程序暂停运行！')
                elif '您的账号访问超频，请稍后访问或联系客服人员' in res:
                    print('账号访问超频，请更换账号！{cc_judge}')
                    input('程序暂停运行！')
                else:
                    tree = etree.HTML(res)
                    try:
                        count_cc = tree.xpath('//div[@class="tcaption"]/h3[contains(text(),"[信用中国]")]/following-sibling::span[1]/text()')[0]
                        count_cc = int(count_cc)
                    except:
                        count_cc = 0
                    localtime = tm().get_localtime()  # 当前时间
                    print(localtime)
                    if count_cc == 0:
                        print(f'计数器：{count}\n公司ID:{com_id}\n行政许可信息[工商局]条数：无')
                    else:
                        print(f'计数器：{count}\n公司ID:{com_id}\n行政许可信息[工商局]条数：{count_cc}')
                    status_column = 'status_credit_adm_license_cc'  # 表字段名
                    count_column = 'count_credit_adm_license_cc'  # 表字段名
                    cd.upd_status(com_id, status_column, count_column, count_cc)
        return com_id, com_name, count_cc

    def get_page_info(self):  # 解析页面内容
        global project_name,license_status,license_content,expire_time,approval_category,area
        alb = AdmLicenseCc()
        value = alb.cc_judge()
        com_id = value[0]
        com_name = value[1]
        count_cc = value[2]
        key = dk().search_key(com_name)
        count = 0
        index_url = 'https://www.qichacha.com'
        page_url = f'{index_url}/company_getinfos?unique={com_id}&companyname={key}&p={page}&tab=run'
        hds = gh().header()
        hds.update({'Referer': f'{index_url}/firm_{com_id}.html'})
        time.sleep(random.randint(3, 5))
        res = requests.get(page_url, headers=hds).text
        if '<script>window.location.href' in res:
            print('访问频繁，需验证！{cc_judge}')
            input('暂停')
        elif '<script>location.href="/user_login"</script>' in res:
            print('Cookie失效，需更换！{cc_judge}')
            input('程序暂停运行！')
        elif '您的账号访问超频，请稍后访问或联系客服人员' in res:
            print('账号访问超频，请更换账号！{cc_judge}')
            input('程序暂停运行！')
        else:
            tree = etree.HTML(res)
            content_li = tree.xpath('//div[@class="tcaption"]/span[contains(text(),"[信用中国]")]/parent::div/following-sibling::table[@class="ntable ntable-odd"]/tr[position()>2]')
            for nbr, content in enumerate(content_li, 1):
                count += 1
                try:
                    license_num = content.xpath('td[1]/text()')[0]
                    dec_book_num = content.xpath('td[2]/text()')[0]
                    license_office = content.xpath('td[3]/text()')[0]
                    dec_date = content.xpath('td[4]/text()')[0]
                    time.sleep(random.randint(1, 2))
                    dt_id = content.xpath('td[5]/a[@class="xzxukeView"]/@onclick')[0].split('xzxukeView("')[1].split('")')[0]
                    dt_url = 'https://www.qichacha.com/company_xzxukeView'
                    para = {'id':f'{dt_id}'}
                    res_info = requests.post(dt_url, headers=hds,data=para).text
                    status = json.loads(res_info)['status']
                    if status == 200:
                        data = json.loads(res_info)['data']
                        project_name = data['name']
                        license_status = data['status']
                        license_content = data['content']
                        expire_time = data['expire_time']
                        approval_category = data['type']
                        area = data['province']
                    else:
                        print(f'响应失败！\n状态码：{status}')
                        input('程序暂停运行！')
                except:
                    license_num = None
                    dec_book_num = None
                    license_office = None
                    dec_date = None
                    dt_id = None
                    project_name = None
                    license_status = None
                    license_content = None
                    expire_time = None
                    approval_category = None
                print('\n{0}--总第{1}条----{2}/{3}页--{0}\n'.format('-' * 9, count, page, count_page))
                localtime = tm().get_localtime()  # 当前时间
                create_time = localtime
                print(f'当前时间：{create_time}')
                print(f'公司ID：{com_id}\n序号:{license_num}\n决定文书号:{dec_book_num}\n许可机关:{license_office}\n详情ID:{dt_id}\n'
                      f'决定日期:{dec_date}\n项目名称:{project_name}\n许可状态:{license_status}\n许可内容:{license_content}\n截止时间:{expire_time}\n'
                      f'审批类别:{approval_category}\n地域:{area}\n创建/入库时间:{create_time}')
                input('Pause')





if __name__ == '__main__':
    cc = AdmLicenseCc()
    cc.get_page_info()