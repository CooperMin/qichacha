#! /usr/bin/env python3
import time

from support.use_mysql import ConnMysql as db


class BaseInfoParse(object):
    def __init__(self, tree):
        self.db = db()
        self.tree = tree
        self.index_url = 'https://www.qichacha.com'

    def verify_ori_type(self):  # 判断组织类型
        tree = self.tree
        try:
            word = tree.xpath('//div[@class="row tags"]/span[contains(@class,"ntag text-pl")]/text()')[0].strip()
        except:
            word = None
        if word in ['社会组织', '事业单位', '学校', '基金会', '香港企业', '台湾企业', '律所', '医院']:
            ori_type = word
        else:
            # 根据经营状态是否存在判断是大陆企业还是其它未被标记的事业单位，存在经营状态则为大陆企业
            status = tree.xpath('//div[@class="row tags"]/span/@class="ntag text-success tooltip-br"')
            # print(status)
            if status is True:
                ori_type = '大陆企业'
            else:
                status = tree.xpath('//div[@class="row tags"]/span/@class="ntag text-success"')
                if status is True:
                    ori_type = '未被标记的港澳企业'
                else:
                    status = tree.xpath('//div[@class="row tags"]/span/@class="ntag text-danger tooltip-br"')
                    if status is True:
                        ori_type = '大陆企业'
                    else:
                        ori_type = '未被标记的企事业单位/律所'
        return ori_type

    def verify_is_listed(self):
        tree = self.tree
        # 根据primary_value 返回的布尔值判断是否是高新技术企业，如果 primary_value 是True,则是高新技术企业
        primary_value = tree.xpath('//div[@class="row tags"]/span/@class="ntag text-primary"')
        if primary_value is True:
            primary = tree.xpath('//div[@class="row tags"]/span[@class="ntag text-primary"]/text()')[0].strip()
        else:
            primary = None
        # 根据investor_value 返回的布尔值判断是否是投资机构， 如果 investor_value 是True,则是投资机构
        investor_value = tree.xpath('//div[@class="row tags"]/a/span/@class="ntag text-warning click"')
        if investor_value is True:
            investor = tree.xpath('//div[@class="row tags"]/a/span[@class="ntag text-warning click"]/text()')[0].strip()
            investor_url = "".join((self.index_url, tree.xpath('//div[@class="row tags"]/a/@href')[0]))
        else:
            investor = None
            investor_url = None
        # 根据is_listed 返回的布尔值判断是否上市或者被投轮次， 如果 is_listed 是True,则已上市或有被投轮次信息
        is_listed = tree.xpath('//span/@class="ntag text-list click"')
        if is_listed is True:
            listed_pool = tree.xpath('//span[@class="ntag text-list click"]/text()')
            listed_pool_new = []
            for listed in listed_pool:
                listed = listed.strip()
                if listed == '':
                    pass
                else:
                    listed_pool_new.append(listed)
            listed_pool = listed_pool_new
            # 判断是否上市，新三板 法理上不算上市公司，但在此处被列为上市公司
            if 'A股' in listed_pool \
                    or '港股' in listed_pool \
                    or '中概股' in listed_pool \
                    or '新三板' in listed_pool \
                    or '科创板' in listed_pool:
                listed_status = True
            else:
                listed_status = False
        else:
            listed_status = False
            listed_pool = []
        return primary, investor, investor_url, is_listed, listed_status, listed_pool

    def common_word(self):
        tree = self.tree
        com_name = tree.xpath('//input[@name="toCompanyName"]/@value')[0].strip().replace('（', '(').replace('）', ')')
        try:
            tel = tree.xpath('//span[contains(text(),"电话：") and @class="cdes"]/following-sibling::span[1]/span')[
                0].text.strip()  # 电话
        except:
            tel = tree.xpath('//span[contains(text(),"电话：") and @class="cdes"]/following-sibling::span[1]')[
                0].text.strip()  # 电话
        try:
            email = tree.xpath('//span[contains(text(),"邮箱：")]/following-sibling::span[1]/a')[0].text.strip()  # 邮箱
            if '...' in email:
                email = tree.xpath('//span[contains(text(),"邮箱：")]/following-sibling::span[1]/a/@href')[0].strip().replace('mailto:','')  # 邮箱
        except:
            email = tree.xpath('//span[contains(text(),"邮箱：")]/following-sibling::span[1]')[0].text.strip()  # 邮箱
        try:
            site = tree.xpath('//span[contains(text(),"官网：")]/following-sibling::span[1]/a')[0].text.strip().strip(
                '\\')  # 官网
        except:
            site = tree.xpath('//span[contains(text(),"官网：")]/following-sibling::span[1]')[0].text.strip().strip(
                '\\')  # 官网
        try:
            try:
                address = tree.xpath('//span[contains(text(),"地址：")]/following-sibling::span[1]/a')[
                    0].text.strip()  # 地址
            except:
                address = tree.xpath('//span[contains(text(),"地址：")]/following-sibling::span[1]')[0].text.strip()
        except:
            address = tree.xpath('//span[contains(text(),"地址：")]/parent/span[2]/a[1]')[0].text.strip()
        intro = tree.xpath('string(//*[@id="jianjieModal"]/div[@class="modal-dialog nmodal"]/div['
                           '@class="modal-content"]/div[@class="modal-body"])').replace('"', '·').strip()
        try:
            count_ipr = tree_us.xpath('string(//*[@id="assets_title"])').split('知识产权')[1].strip()
            if count_ipr == '999+':
                count_ipr = '1000'
        except:
            count_ipr = '0'
        try:
            count_tm = tree.xpath(
                '//*[@class="company-nav-items"]/a[contains(text(),"商标信息")]/span|//*[@class="company-nav-items"]/span[contains(text(),"商标信息")]/span')[
                0].text.strip()
            if count_tm == '999+':
                count_tm = '1000'
        except:
            count_tm = '0'
        try:
            count_patent = tree.xpath(
                '//*[@class="company-nav-items"]/a[contains(text(),"专利信息")]/span|//*[@class="company-nav-items"]/span[contains(text(),"专利信息")]/span')[
                0].text.strip()
            if count_patent == '999+':
                count_patent = '1000'
        except:
            count_patent = '0'
        try:
            count_cer = tree.xpath(
                '//*[@class="company-nav-items"]/a[contains(text(),"证书信息")]/span|//*[@class="company-nav-items"]/span[contains(text(),"证书信息")]/span')[
                0].text.strip()
            if count_cer == '999+':
                count_cer = '1000'
        except:
            count_cer = '0'
        try:
            count_cpr_of_works = tree.xpath(
                '//*[@class="company-nav-items"]/a[contains(text(),"作品著作权")]/span|//*[@class="company-nav-items"]/span[contains(text(),"作品著作权")]/span')[
                0].text.strip()
            if count_cpr_of_works == '999+':
                count_cpr_of_works = '1000'
        except:
            count_cpr_of_works = '0'
        try:
            count_cpr_of_soft = tree.xpath(
                '//*[@class="company-nav-items"]/a[contains(text(),"软件著作权")]/span|//*[@class="company-nav-items"]/span[contains(text(),"软件著作权")]/span')[
                0].text.strip()
            if count_cpr_of_soft == '999+':
                count_cpr_of_soft = '1000'
        except:
            count_cpr_of_soft = '0'
        try:
            count_web = tree.xpath(
                '//*[@class="company-nav-items"]/a[contains(text(),"网站信息")]/span|//*[@class="company-nav-items"]/span[contains(text(),"网站信息")]/span')[
                0].text.strip()
            if count_web == '999+':
                count_web = '1000'
        except:
            count_web = '0'
        return com_name, tel, email, site, address, intro, count_ipr, count_tm, count_patent, count_cer, count_cpr_of_works, count_cpr_of_soft, count_web

    def land_com(self, result, basic, ori_type, com_id, kw, num, company_count):
        tree = self.tree
        high_tech = result[0]
        investor = result[1]
        investor_url = result[2]
        is_listed = result[3]
        listed_status = result[4]
        listed_pool = result[5]
        if is_listed is listed_status is True:
            is_listed = True
        else:
            is_listed = False
        com_name = basic[0]
        tel = basic[1]
        email = basic[2]
        site = basic[3]
        address = basic[4]
        intro = basic[5]
        count_ipr = basic[6]
        count_tm = basic[7]
        count_patent = basic[8]
        count_cer = basic[9]
        count_cpr_of_works = basic[10]
        count_cpr_of_soft = basic[11]
        count_web = basic[11]
        try:
            legal_person = tree.xpath('//h2[@class="seo font-20" or @class="seo font-15"]/text()')[0].strip()
        except:
            try:
                legal_person = tree.xpath('//div[@class="boss-td"]/div/p/text()')[0].strip()
            except:
                legal_person = tree.xpath('//div[@class="boss-td"]/a/text()')[0].strip()
        reg_cap = tree.xpath('//td[contains(text(),"注册资本")]/following-sibling::td[1]')[0].text.strip()
        paid_in_cap = tree.xpath('//td[contains(text(),"实缴资本")]/following-sibling::td[1]')[0].text.strip()
        management_form = tree.xpath('//td[contains(text(),"经营状态")]/following-sibling::td[1]')[0].text.strip()
        create_date = tree.xpath('//td[contains(text(),"成立日期")]/following-sibling::td[1]')[0].text.strip()
        uscc = tree.xpath('//td[contains(text(),"统一社会信用代码")]/following-sibling::td[1]')[0].text.strip()
        tin = tree.xpath('//td[contains(text(),"纳税人识别号") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        regno = tree.xpath('//td[contains(text(),"注册号") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        occ = tree.xpath('//td[contains(text(),"组织机构代码") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        com_type = tree.xpath('//td[contains(text(),"企业类型") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        industry = tree.xpath('//td[contains(text(),"所属行业")]/following-sibling::td[1]')[0].text.strip()
        approval_date = tree.xpath('//td[contains(text(),"核准日期") and @class="tb"]/following-sibling::td[1]')[
            0].text.strip()
        reg_auth = tree.xpath('//td[contains(text(),"登记机关") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        area = tree.xpath('//td[contains(text(),"所属地区") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        com_en_name = tree.xpath('//td[contains(text(),"英文名")]/following-sibling::td[1]')[0].text.strip()
        com_used_name = tree.xpath('//td[contains(text(),"曾用名")]/following-sibling::td[1]')[0].text.strip()
        try:
            insured = tree.xpath('//td[contains(text(),"参保人数")]/following-sibling::td[1]')[0].text.strip()
        except:
            insured = '-'
        com_size = tree.xpath('//td[contains(text(),"人员规模")]/following-sibling::td[1]')[0].text.strip()
        business_term = tree.xpath('//td[contains(text(),"营业期限") and @class="tb"]/following-sibling::td[1]')[
            0].text.strip()
        scope_of_business = tree.xpath('//td[contains(text(),"经营范围") and @class="tb"]/following-sibling::td[1]')[
            0].text.strip().strip('\\').replace('"', "'")
        print('\n{0}{1}/{2}{0}'.format('-' * 30, num, company_count))
        localtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # 当前时间
        print(f'当前时间：{localtime}\n公司ID：{com_id}')
        print(f'公司名称：{com_name}\n电话：{tel}\n邮箱：{email}\n官网：{site}\n地址：{address}\n组织类型：{ori_type}\n'
              f'是否高新技术企业：{high_tech}\n是否投资机构：{investor}\n投资机构页面：{investor_url}\n是否上市：{is_listed}\n上市/融资标签：{listed_pool}\n'
              f'统一社会信用代码：{uscc}\n纳税人识别号：{tin}\n注册号：{regno}\n组织机构代码：{occ}\n经营状态：{management_form}\n'
              f'公司类型：{com_type}\n成立日期：{create_date}\n法人：{legal_person}\n注册资本：{reg_cap}\n实缴资本：{paid_in_cap}\n'
              f'营业期限：{business_term}\n登记机关：{reg_auth}\n核准日期：{approval_date}\n公司规模：{com_size}\n所属行业：{industry}\n公司英文名：{com_en_name}\n'
              f'曾用名：{com_used_name}\n所属地区：{area}\n参保人数：{insured}\n经营范围：{scope_of_business}\n公司介绍：{intro}\n'
              f'知识产权：{count_ipr}\n'
              f'商标信息：{count_tm}\n专利信息：{count_patent}\n证书信息：{count_cer}\n作品著作权：{count_cpr_of_works}\n软件著作权：{count_cpr_of_soft}\n'
              f'网站信息：{count_web}\n')
        ins = f"""INSERT INTO `com_info_init` 
        (com_id,com_name,ori_type,high_tech,investor,
         investor_url,is_listed,listed_pool,tel,email,
         site,address,legal_person,reg_cap,paid_in_cap,
         management_form,create_date,uscc,tin,regno,
         occ,com_type,industry,approval_date,reg_auth,
         area,com_en_name,com_used_name,insured,com_size,
         business_term,scope_of_business,intro,kw,count_ipr,
         count_tm,count_patent,count_cer,count_cpr_of_works,count_cpr_of_soft,count_web,create_time)
        VALUES 
        ("{com_id}","{com_name}","{ori_type}","{high_tech}","{investor}",
         "{investor_url}","{is_listed}","{listed_pool}","{tel}","{email}",
         "{site}","{address}","{legal_person}","{reg_cap}","{paid_in_cap}",
         "{management_form}","{create_date}","{uscc}","{tin}","{regno}",
         "{occ}","{com_type}","{industry}","{approval_date}","{reg_auth}",
         "{area}","{com_en_name}","{com_used_name}","{insured}","{com_size}",
         "{business_term}","{scope_of_business}","{intro}","{kw}","{count_ipr}",
         "{count_tm}","{count_patent}","{count_cer}","{count_cpr_of_works}","{count_cpr_of_soft}","{count_web}",now()
        );
        """
        self.db.inssts(ins)



    def hk_com(self, result, basic, ori_type, com_id, kw, num, company_count):
        tree = self.tree
        high_tech = result[0]
        investor = result[1]
        investor_url = result[2]
        is_listed = result[3]
        listed_status = result[4]
        listed_pool = result[5]
        if is_listed is listed_status is True:
            is_listed = True
        else:
            is_listed = False
        com_name = basic[0]
        tel = basic[1]
        email = basic[2]
        site = basic[3]
        address = basic[4]
        intro = basic[5]
        count_ipr = basic[6]
        count_tm = basic[7]
        count_patent = basic[8]
        count_cer = basic[9]
        count_cpr_of_works = basic[10]
        count_cpr_of_soft = basic[11]
        count_web = basic[11]
        legal_person = tree.xpath('//td[contains(text(),"董事长") and @class="tb"]/following-sibling::td[1]')[
            0].text.strip()
        reg_cap = tree.xpath('//td[contains(text(),"股本") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        uscc = tree.xpath('//td[contains(text(),"公司编号") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        com_type = tree.xpath('//td[contains(text(),"公司类别") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        create_date = tree.xpath('//td[contains(text(),"成立日期") and @class="tb"]/following-sibling::td[1]')[
            0].text.strip()
        management_form = tree.xpath('//td[contains(text(),"公司现况") and @class="tb"]/following-sibling::td[1]')[
            0].text.strip()
        liquidation_model = tree.xpath('//td[contains(text(),"清盘模式") and @class="tb"]/following-sibling::td[1]')[
            0].text.strip()
        date_of_dissolution = \
        tree.xpath('//td[contains(text(),"已告解散日期/不再是独立实体日期") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        reg_of_change = tree.xpath('//td[contains(text(),"押记登记册") and @class="tb"]/following-sibling::td[1]')[
            0].text.strip()
        important_notes = tree.xpath('//td[contains(text(),"重要事项") and @class="tb"]/following-sibling::td[1]')[
            0].text.strip()
        print('\n{0}{1}/{2}{0}'.format('-' * 30, num, company_count))
        localtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # 当前时间
        print(f'当前时间：{localtime}\n公司ID：{com_id}')
        print(f'公司名称：{com_name}\n电话：{tel}\n邮箱：{email}\n官网：{site}\n地址：{address}\n组织类型：{ori_type}\n'
              f'是否高新技术企业：{high_tech}\n是否投资机构：{investor}\n投资机构页面：{investor_url}\n是否上市：{is_listed}\n上市/融资标签：{listed_pool}\n'
              f'统一社会信用代码：{uscc}\n经营状态：{management_form}\n清盘模式：{liquidation_model}\n已告解散日期/不再是独立实体日期：{date_of_dissolution}\n押记登记册：{reg_of_change}\n'
              f'公司类型：{com_type}\n成立日期：{create_date}\n法人：{legal_person}\n注册资本：{reg_cap}\n'
              f'重要事项：{important_notes}\n公司介绍：{intro}\n知识产权：{count_ipr}\n商标信息：{count_tm}\n'
              f'专利信息：{count_patent}\n证书信息：{count_cer}\n作品著作权：{count_cpr_of_works}\n软件著作权：{count_cpr_of_soft}\n网站信息：{count_web}\n')
        ins = f"""INSERT INTO `com_info_init` 
        (com_id,com_name,ori_type,high_tech,investor,
         investor_url,is_listed,listed_pool,tel,email,
         site,address,legal_person,management_form,liquidation_model,
         date_of_dissolution,reg_of_change,create_date,reg_cap,uscc,
         com_type,important_notes,intro,kw,count_ipr,
         count_tm,count_patent,count_cer,count_cpr_of_works,count_cpr_of_soft,count_web,create_time)
        VALUES 
        ("{com_id}","{com_name}","{ori_type}","{high_tech}","{investor}",
         "{investor_url}","{is_listed}","{listed_pool}","{tel}","{email}",
         "{site}","{address}","{legal_person}","{management_form}","{liquidation_model}",
         "{date_of_dissolution}","{reg_of_change}","{create_date}","{reg_cap}","{uscc}",
         "{com_type}","{important_notes}","{intro}","{kw}","{count_ipr}",
         "{count_tm}","{count_patent}","{count_cer}","{count_cpr_of_works}","{count_cpr_of_soft}","{count_web}",now()
        );
        """
        self.db.inssts(ins)


    def tw_com(self, result, basic, ori_type, com_id, kw, num, company_count):
        tree = self.tree
        high_tech = result[0]
        investor = result[1]
        investor_url = result[2]
        is_listed = result[3]
        listed_status = result[4]
        listed_pool = result[5]
        if is_listed is listed_status is True:
            is_listed = True
        else:
            is_listed = False
        com_name = basic[0]
        tel = basic[1]
        email = basic[2]
        site = basic[3]
        address = basic[4]
        intro = basic[5]
        count_ipr = basic[6]
        count_tm = basic[7]
        count_patent = basic[8]
        count_cer = basic[9]
        count_cpr_of_works = basic[10]
        count_cpr_of_soft = basic[11]
        count_web = basic[11]
        legal_person = tree.xpath('//td[contains(text(),"代表人姓名") and @class="tb"]/following-sibling::td[1]/a')[0].text.strip()
        uscc = tree.xpath('//td[contains(text(),"统一编号") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        reg_cap = tree.xpath('//td[contains(text(),"资本总额") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        paid_in_cap = tree.xpath('//td[contains(text(),"实收资本额") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        management_form = tree.xpath('//td[contains(text(),"公司状况") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        reg_auth = tree.xpath('//td[contains(text(),"登记机关") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        equity_status = tree.xpath('//td[contains(text(),"股权状态") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        com_en_name = tree.xpath('//td[contains(text(),"英文名称") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        create_date = tree.xpath('//td[contains(text(),"核准设立日期") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        approval_date = tree.xpath('//td[contains(text(),"最后核准变更日期") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        scope_of_business = tree.xpath('//td[contains(text(),"营业范围") and @class="tb"]/following-sibling::td[1]')[0].text.strip().strip('\\').replace('"', "'")
        print('\n{0}{1}/{2}{0}'.format('-' * 30, num, company_count))
        localtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # 当前时间
        print(f'当前时间：{localtime}\n公司ID：{com_id}')
        print(f'公司名称：{com_name}\n电话：{tel}\n邮箱：{email}\n官网：{site}\n地址：{address}\n组织类型：{ori_type}\n'
              f'是否高新技术企业：{high_tech}\n是否投资机构：{investor}\n投资机构页面：{investor_url}\n是否上市：{is_listed}\n上市/融资标签：{listed_pool}\n'
              f'统一社会信用代码：{uscc}\n经营状态：{management_form}\n股权状态：{equity_status}\n公司英文名：{com_en_name}\n'
              f'成立日期：{create_date}\n法人：{legal_person}\n注册资本：{reg_cap}\n实收资本额：{paid_in_cap}\n核准日期：{approval_date}\n'
              f'登记机关：{reg_auth}\n经营范围：{scope_of_business}\n公司介绍：{intro}\n知识产权：{count_ipr}\n商标信息：{count_tm}\n'
              f'专利信息：{count_patent}\n证书信息：{count_cer}\n作品著作权：{count_cpr_of_works}\n软件著作权：{count_cpr_of_soft}\n网站信息：{count_web}\n')
        ins = f"""INSERT INTO `com_info_init` 
        (com_id,com_name,ori_type,high_tech,investor,
         investor_url,is_listed,listed_pool,tel,email,
         site,address,legal_person,management_form,paid_in_cap,
         reg_auth,equity_status,create_date,reg_cap,uscc,
         com_en_name,approval_date,scope_of_business,intro,kw,count_ipr,
         count_tm,count_patent,count_cer,count_cpr_of_works,count_cpr_of_soft,count_web,create_time)
        VALUES 
        ("{com_id}","{com_name}","{ori_type}","{high_tech}","{investor}",
         "{investor_url}","{is_listed}","{listed_pool}","{tel}","{email}",
         "{site}","{address}","{legal_person}","{management_form}","{paid_in_cap}",
         "{reg_auth}","{equity_status}","{create_date}","{reg_cap}","{uscc}",
         "{com_en_name}","{approval_date}","{scope_of_business}","{intro}","{kw}","{count_ipr}",
         "{count_tm}","{count_patent}","{count_cer}","{count_cpr_of_works}","{count_cpr_of_soft}","{count_web}",now()
        );
        """
        self.db.inssts(ins)

    def social_ori(self, basic, ori_type, com_id, kw, num, company_count):
        tree = self.tree
        com_name = basic[0]
        tel = basic[1]
        email = basic[2]
        site = basic[3]
        address = basic[4]
        intro = basic[5]
        count_ipr = basic[6]
        count_tm = basic[7]
        count_patent = basic[8]
        count_cer = basic[9]
        count_cpr_of_works = basic[10]
        count_cpr_of_soft = basic[11]
        count_web = basic[11]
        legal_person = tree.xpath('//td[contains(text(),"法人/负责人") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        uscc = tree.xpath('//td[contains(text(),"统一社会信用代码") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        reg_cap = tree.xpath('//td[contains(text(),"注册资本") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        create_date = tree.xpath('//td[contains(text(),"成立日期") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        management_form = tree.xpath('//td[contains(text(),"登记状态") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        com_type = tree.xpath('//td[contains(text(),"社会组织类型") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        reg_auth = tree.xpath('//td[contains(text(),"登记机关") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        issuing_authority = tree.xpath('//td[contains(text(),"发证机关") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        business_term = tree.xpath('//td[contains(text(),"证书有效期") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        scope_of_business = tree.xpath('//td[contains(text(),"业务范围") and @class="tb"]/following-sibling::td[1]')[0].text.strip().strip('\\').replace('"', "'")
        print('\n{0}{1}/{2}{0}'.format('-' * 30, num, company_count))
        localtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # 当前时间
        print(f'当前时间：{localtime}\n公司ID：{com_id}')
        print(f'公司名称：{com_name}\n电话：{tel}\n邮箱：{email}\n官网：{site}\n地址：{address}\n组织类型：{ori_type}\n'
              f'统一社会信用代码：{uscc}\n公司类型：{com_type}\n经营状态：{management_form}\n'
              f'成立日期：{create_date}\n法人：{legal_person}\n注册资本：{reg_cap}\n登记机关：{reg_auth}\n发证机关：{issuing_authority}\n'
              f'营业期限：{business_term}\n经营范围：{scope_of_business}\n公司介绍：{intro}\n知识产权：{count_ipr}\n商标信息：{count_tm}\n'
              f'专利信息：{count_patent}\n证书信息：{count_cer}\n作品著作权：{count_cpr_of_works}\n软件著作权：{count_cpr_of_soft}\n网站信息：{count_web}\n')
        ins = f"""INSERT INTO `com_info_init` 
        (com_id,com_name,ori_type,tel,email,
         site,address,legal_person,management_form,issuing_authority,
         reg_auth,create_date,reg_cap,uscc,com_type,
         business_term,scope_of_business,intro,kw,count_ipr,
         count_tm,count_patent,count_cer,count_cpr_of_works,count_cpr_of_soft,count_web,create_time)
        VALUES 
        ("{com_id}","{com_name}","{ori_type}","{tel}","{email}",
         "{site}","{address}","{legal_person}","{management_form}","{issuing_authority}",
         "{reg_auth}","{create_date}","{reg_cap}","{uscc}","{com_type}",
         "{business_term}","{scope_of_business}","{intro}","{kw}","{count_ipr}",
         "{count_tm}","{count_patent}","{count_cer}","{count_cpr_of_works}","{count_cpr_of_soft}","{count_web}",now()
        );
        """
        self.db.inssts(ins)


    def foundation(self, basic, ori_type, com_id, kw, num, company_count):
        tree = self.tree
        com_name = basic[0]
        tel = basic[1]
        email = basic[2]
        site = basic[3]
        address = basic[4]
        intro = basic[5]
        count_ipr = basic[6]
        count_tm = basic[7]
        count_patent = basic[8]
        count_cer = basic[9]
        count_cpr_of_works = basic[10]
        count_cpr_of_soft = basic[11]
        count_web = basic[11]
        legal_person = tree.xpath('//td[contains(text(),"理事长") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        syg = tree.xpath('//td[contains(text(),"秘书长") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        linkman = tree.xpath('//td[contains(text(),"对外联系人姓名") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        linkman_position = tree.xpath('//td[contains(text(),"联系人职务") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        uscc = tree.xpath('//td[contains(text(),"信用代码") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        occ = tree.xpath('//td[contains(text(),"组织机构代码") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        reg_cap = tree.xpath('//td[contains(text(),"原始基金") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        com_used_name = tree.xpath('//td[contains(text(),"曾用名") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        com_en_name = tree.xpath('//td[contains(text(),"基金会英文名称") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        purpose = tree.xpath('//td[contains(text(),"宗旨") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        scope_of_business = tree.xpath('//td[contains(text(),"业务范围") and @class="tb"]/following-sibling::td[1]')[0].text.strip().strip('\\').replace('"', "'")
        focus_fields = tree.xpath('//td[contains(text(),"关注领域") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        gov_body = tree.xpath('//td[contains(text(),"业务主管单位") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        scope_of_foundation = tree.xpath('//td[contains(text(),"基金会范围") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        reg_auth = tree.xpath('//td[contains(text(),"登记部门") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        create_date = tree.xpath('//td[contains(text(),"成立日期") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        zip_code = tree.xpath('//td[contains(text(),"邮政编码") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        leader_in_country_count = tree.xpath('//td[contains(text(),"负责人中国家工作人数") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        leader_in_province_count = tree.xpath('//td[contains(text(),"责任人中担任过省部级工作人员数") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        full_time_staff_count = tree.xpath('//td[contains(text(),"全职员工数量") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        volunteer_count = tree.xpath('//td[contains(text(),"志愿者数量") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        assess_level = tree.xpath('//td[contains(text(),"评估等级") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        spe_fund_count = tree.xpath('//td[contains(text(),"专项基金数") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        preferential_qualification_types = tree.xpath('//td[contains(text(),"优惠资格类型") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        print('\n{0}{1}/{2}{0}'.format('-' * 30, num, company_count))
        localtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # 当前时间
        print(f'当前时间：{localtime}\n公司ID：{com_id}')
        print(f'公司名称：{com_name}\n电话：{tel}\n邮箱：{email}\n邮编：{zip_code}\n官网：{site}\n地址：{address}\n组织类型：{ori_type}\n'
              f'统一社会信用代码：{uscc}\n组织机构代码：{occ}\n成立日期：{create_date}\n法人：{legal_person}\n'
              f'秘书长：{syg}\n对外联系人：{linkman}\n对外联系人职务：{linkman_position}\n基金会曾用名：{com_used_name}\n基金会英文名：{com_en_name}\n'
              f'注册资本：{reg_cap}\n登记机关：{reg_auth}\n关注领域：{focus_fields}\n业务主管单位：{gov_body}\n宗旨：{purpose}\n'
              f'基金会范围：{scope_of_foundation}\n经营范围：{scope_of_business}\n公司介绍：{intro}\n负责人中国家工作人数：{leader_in_country_count}\n负责人中担任过省部级工作人员数：{leader_in_province_count}\n'
              f'全职员工数量：{full_time_staff_count}\n志愿者数量：{volunteer_count}\n评估等级：{assess_level}\n专项基金数：{spe_fund_count}\n优惠资格类型：{preferential_qualification_types}\n知识产权：{count_ipr}\n商标信息：{count_tm}\n'
              f'专利信息：{count_patent}\n证书信息：{count_cer}\n作品著作权：{count_cpr_of_works}\n软件著作权：{count_cpr_of_soft}\n网站信息：{count_web}\n')
        ins = f"""INSERT INTO `com_info_init`
        (com_id,com_name,ori_type,tel,email,
         site,address,legal_person,syg,linkman,
         linkman_job,reg_auth,com_used_name,com_en_name,create_date,
         reg_cap,uscc,occ,purpose,scope_of_business,
         focus_fields,gov_body,scope_of_foundation,zip_code,leader_in_country_count,
         leader_in_province_count,full_time_staff_count,volunteer_count,assess_level,spe_fund_count,
         preferential_qualification_types,intro,kw,count_ipr,count_tm,
         count_patent,count_cer,count_cpr_of_works,count_cpr_of_soft,count_web,create_time)
        VALUES 
        ("{com_id}","{com_name}","{ori_type}","{tel}","{email}",
         "{site}","{address}","{legal_person}","{syg}","{linkman}",
         "{linkman_position}","{reg_auth}","{com_used_name}","{com_en_name}","{create_date}",
         "{reg_cap}","{uscc}","{occ}","{purpose}","{scope_of_business}",
         "{focus_fields}","{gov_body}","{scope_of_foundation}","{zip_code}","{leader_in_country_count}",
         "{leader_in_province_count}","{full_time_staff_count}","{volunteer_count}","{assess_level}","{spe_fund_count}",
         "{preferential_qualification_types}","{intro}","{kw}","{count_ipr}","{count_tm}",
         "{count_patent}","{count_cer}","{count_cpr_of_works}","{count_cpr_of_soft}","{count_web}",now()
        );
        """
        self.db.inssts(ins)

    def public_institution(self, basic, ori_type, com_id, kw, num, company_count):
        tree = self.tree
        com_name = basic[0]
        tel = basic[1]
        email = basic[2]
        site = basic[3]
        address = basic[4]
        intro = basic[5]
        count_ipr = basic[6]
        count_tm = basic[7]
        count_patent = basic[8]
        count_cer = basic[9]
        count_cpr_of_works = basic[10]
        count_cpr_of_soft = basic[11]
        count_web = basic[11]
        try:
            legal_person = tree.xpath('//h2[@class="seo font-20" or @class="seo font-15"]/text()')[0].strip()
        except:
            legal_person = tree.xpath('//div[@class="boss-td"]/div/p/text()')[0].strip()
        reg_cap = tree.xpath('//td[contains(text(),"开办资金")]/following-sibling::td[1]')[0].text.strip()
        uscc = tree.xpath('//td[contains(text(),"统一社会信用代码")]/following-sibling::td[1]')[0].text.strip()
        management_form = tree.xpath('//td[contains(text(),"经营状态")]/following-sibling::td[1]')[0].text.strip()
        reg_auth = tree.xpath('//td[contains(text(),"登记机关") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        business_unit_in_charge = tree.xpath('//td[contains(text(),"举办单位") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        business_term = tree.xpath('//td[contains(text(),"有效期") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        sources_of_funds = tree.xpath('//td[contains(text(),"经费来源") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        scope_of_business = tree.xpath('//td[contains(text(),"宗旨和业务范围") and @class="tb"]/following-sibling::td[1]')[0].text.strip().strip('\\').replace('"', "'")
        print('\n{0}{1}/{2}{0}'.format('-' * 30, num, company_count))
        localtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # 当前时间
        print(f'当前时间：{localtime}\n公司ID：{com_id}')
        print(f'公司名称：{com_name}\n电话：{tel}\n邮箱：{email}\n官网：{site}\n地址：{address}\n组织类型：{ori_type}\n'
              f'统一社会信用代码：{uscc}\n法人：{legal_person}\n注册资本：{reg_cap}\n经费来源：{sources_of_funds}\n登记机关：{reg_auth}\n'
              f'经营状态：{management_form}\n举办单位：{business_unit_in_charge}\n有效期：{business_term}\n经营范围：{scope_of_business}\n公司介绍：{intro}\n'
              f'知识产权：{count_ipr}\n商标信息：{count_tm}\n'
              f'专利信息：{count_patent}\n证书信息：{count_cer}\n作品著作权：{count_cpr_of_works}\n软件著作权：{count_cpr_of_soft}\n网站信息：{count_web}\n')
        ins = f"""INSERT INTO `com_info_init` 
        (com_id,com_name,ori_type,tel,email,
         site,address,legal_person,management_form,
         reg_auth,reg_cap,uscc,business_unit_in_charge,
         business_term,sources_of_funds,scope_of_business,intro,kw,count_ipr,
         count_tm,count_patent,count_cer,count_cpr_of_works,count_cpr_of_soft,count_web,create_time)
        VALUES 
        ("{com_id}","{com_name}","{ori_type}","{tel}","{email}",
         "{site}","{address}","{legal_person}","{management_form}",
         "{reg_auth}","{reg_cap}","{uscc}","{business_unit_in_charge}",
         "{business_term}","{sources_of_funds}","{scope_of_business}","{intro}","{kw}","{count_ipr}",
         "{count_tm}","{count_patent}","{count_cer}","{count_cpr_of_works}","{count_cpr_of_soft}","{count_web}",now()
        );
        """
        self.db.inssts(ins)

    def law_firm(self, basic, ori_type, com_id, kw, num, company_count):
        tree = self.tree
        com_name = basic[0]
        tel = basic[1]
        email = basic[2]
        site = basic[3]
        address = basic[4]
        count_ipr = basic[6]
        count_tm = basic[7]
        count_patent = basic[8]
        count_cer = basic[9]
        count_cpr_of_works = basic[10]
        count_cpr_of_soft = basic[11]
        count_web = basic[11]
        legal_person = tree.xpath('//td[contains(text(),"负责人") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        uscc = tree.xpath('//td[contains(text(),"执业证号") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        create_date = tree.xpath('//td[contains(text(),"成立日期") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        com_size = tree.xpath('//td[contains(text(),"律师人数")]/following-sibling::td[1]')[0].text.strip()
        area = tree.xpath('//td[contains(text(),"所属地区") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        intro = tree.xpath('//td[contains(text(),"机构简介") and @class="tb"]/following-sibling::td[1]')[0].text.strip()
        print('\n{0}{1}/{2}{0}'.format('-' * 30, num, company_count))
        localtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # 当前时间
        print(f'当前时间：{localtime}\n公司ID：{com_id}')
        print(f'公司名称：{com_name}\n电话：{tel}\n邮箱：{email}\n官网：{site}\n地址：{address}\n组织类型：{ori_type}\n'
              f'统一社会信用代码：{uscc}\n法人：{legal_person}\n成立日期：{create_date}\n律师人数：{com_size}\n'
              f'所属地区：{area}\n公司介绍：{intro}\n知识产权：{count_ipr}\n商标信息：{count_tm}\n'
              f'专利信息：{count_patent}\n证书信息：{count_cer}\n作品著作权：{count_cpr_of_works}\n软件著作权：{count_cpr_of_soft}\n网站信息：{count_web}\n')
        ins = f"""INSERT INTO `com_info_init` 
        (com_id,com_name,ori_type,tel,email,
         site,address,legal_person,com_size,area,
         create_date,uscc,intro,kw,count_ipr,
         count_tm,count_patent,count_cer,count_cpr_of_works,count_cpr_of_soft,count_web,create_time)
        VALUES 
        ("{com_id}","{com_name}","{ori_type}","{tel}","{email}",
         "{site}","{address}","{legal_person}","{com_size}","{area}",
         "{create_date}","{uscc}","{intro}","{kw}","{count_ipr}",
         "{count_tm}","{count_patent}","{count_cer}","{count_cpr_of_works}","{count_cpr_of_soft}","{count_web}",now()
        );
        """
        self.db.inssts(ins)

    def choice_parse(self, ori_type):  # land, hk, tw, social, foundation, public, law
        pass
