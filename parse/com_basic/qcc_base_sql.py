#! /usr/bin/env python3

from support.use_mysql import ConnMysql as db


class ins_tb_com(object):
    def __init__(self, arg):
        self.db = db()
        self.arg = arg

    def ins_land_com(self):
        com_id = self.arg[0]
        com_name = self.arg[1]
        ori_type = self.arg[2]
        high_tech = self.arg[3]
        investor = self.arg[4]
        investor_url = self.arg[5]
        is_listed = self.arg[6]
        listed_pool = self.arg[7]
        tel = self.arg[8]
        email = self.arg[9]
        site = self.arg[10]
        address = self.arg[11]
        legal_person = self.arg[12]
        reg_cap = self.arg[13]
        paid_in_cap = self.arg[14]
        management_form = self.arg[15]
        create_date = self.arg[16]
        uscc = self.arg[17]
        tin = self.arg[18]
        regno = self.arg[19]
        occ = self.arg[20]
        com_type = self.arg[21]
        industry = self.arg[22]
        approval_date = self.arg[23]
        reg_auth = self.arg[24]
        area = self.arg[25]
        com_en_name = self.arg[26]
        com_used_name = self.arg[27]
        insured = self.arg[28]
        com_size = self.arg[29]
        business_term = self.arg[30]
        scope_of_business = self.arg[31]
        intro = self.arg[32]
        kw = self.arg[33]
        count_ipr = self.arg[34]
        count_tm = self.arg[35]
        count_patent = self.arg[36]
        count_cer = self.arg[37]
        count_cpr_of_works = self.arg[38]
        count_cpr_of_soft = self.arg[39]
        count_web = self.arg[40]
        print(site,email,address,listed_pool,type(listed_pool))
        ins = f"""
        INSERT INTO 
        `com_info_init` 
        (com_id, com_name, ori_type, high_tech, investor,
         investor_url, is_listed, listed_pool, tel, email,
         site, address, legal_person, reg_cap, paid_in_cap,
         management_form, create_date, uscc, tin, regno,
         occ, com_type, industry, approval_date, reg_auth,
         area, com_en_name, com_used_name, insured, com_size,
         business_term, scope_of_business, intro, origin, `chain`,
         kw, count_ipr, count_tm, count_patent, count_cer,
         count_cpr_of_works, count_cpr_of_soft, count_web, create_time)
         VALUES 
         ({com_id}, {com_name}, {ori_type}, {high_tech}, {investor},
         {investor_url}, {is_listed}, {listed_pool}, {tel}, {email},
         {site}, {address}, {legal_person}, {reg_cap}, {paid_in_cap},
         {management_form}, {create_date}, {uscc}, {tin}, {regno},
         {occ}, {com_type}, {industry}, {approval_date}, {reg_auth},
         {area}, {com_en_name}, {com_used_name}, {insured}, {com_size},
         {business_term}, {scope_of_business}, {intro}, 'origin', 'chain',
         {kw}, {count_ipr}, {count_tm}, {count_patent}, {count_cer},
         {count_cpr_of_works}, {count_cpr_of_soft}, {count_web}, NOW());
        """
        self.db.inssts(ins)


if __name__ == '__main__':
    table_name = 'com_info_init'
    ins = ins_land_com()
    print(ins)
