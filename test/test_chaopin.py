#! /usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import sys
import time
import random
import requests

from support.others import DealKey as dk
from support.headers import GeneralHeaders as gh
from support.cookies import Cookies as ck
from urllib.parse import quote,unquote

# hds = gh().header()
# hds.update({'Referer': 'https://www.qichacha.com'})
# url = 'https://www.qichacha.com/firm_8c17e647be69209f4e1604ddbf8623c2.html'

# res = requests.get(url,headers=hds).text
# cookie = hds['Cookie']
# # print(res)
# print(cookie)



# index_url = 'https://www.qichacha.com'
# com_id = 'sfa79258ba5176322123262f92026aba'
# com_name = '汕头市聿怀初级中学'
# key = dk().search_key(com_name)
# com_url = f'{index_url}/company_getinfos?unique={com_id}&companyname={key}&tab=assets'
# hds = gh().header()
# hds.update({'Referer': f'{index_url}/firm_{com_id}.html'})
# time.sleep(random.randint(1,2))
# res = requests.get(com_url,headers=hds).text
# print(res)

# tim = time.strptime('2019-05-19','%Y-%m-%d')
# tim = round(time.mktime(tim))
#
# print(tim)
# index = 'https://www.qichacha.com/company_getinfos?'
# header = gh().header()
# header.update({'Referer': 'https://www.qichacha.com/firm_88fc0b1d105b03d0bfa1edf37cb9e961.html'})
# para = {
# 'unique':'88fc0b1d105b03d0bfa1edf37cb9e961',
# 'companyname':'TCL集团股份有限公司',
# 'p':1,
# 'tab':'run',
# 'box':'job'}
# res = requests.get(index,params=para,headers=header)
# content = res.text
# url = res.url
# print(url)
# 编码

# for num in range(5001,23712):
#     num = str(num)
#     if int(num) <10:
#         num = '50000'+num
#     elif int(num) <100:
#         num = '5000'+num
#     elif int(num) < 1000:
#         num = '500' + num
#     elif int(num) <10000:
#         num = '50'+num
#     else:
#         num = '5' + num
#     print(num)




# ckli = ck().format_cookie('JSESSIONID=57E863E38F1557CFB089286A06704DC5; tk=ywrtckZE2vftwIEgtXJ4U59SfzQvnGih2Qd82nAow7Ietm1m0; route=c5c62a339e7744272a54643b3be5bf64; BIGipServerotn=116392458.24610.0000; BIGipServerpool_passport=283968010.50215.0000; RAIL_EXPIRATION=1562231697018; RAIL_DEVICEID=U_1tAlKzs-XNg19ezJb5dPcshHIGEOK4c8gDqPmwifsimtr5JMvzhQjm0JVBuIbQ2-mhP12RYM7bD3-CvFueAlaRsWL0-QdguHQ5kQ4LjKAOSUZICNbAJOh2FeZGc41qxUffPOzg37ZD3GDaZoe1oBaeYie52WIy; _jc_save_fromStation=%u9A7B%u9A6C%u5E97%2CZDN; _jc_save_toStation=%u9752%u5C9B%2CQDK; _jc_save_fromDate=2019-07-04; _jc_save_toDate=2019-07-01; _jc_save_wfdc_flag=dc')
# # for k,v in ckli.items():
# #     k = k.strip()
# #     v = unquote(v.strip())
# #
# #     print(f'{k}:{v}')
# k = '%u9A7B%u9A6C%u5E97'
# print(unquote(k))
print(os.getcwd())
print(sys.path)
ll = os.path.dirname('test')
print(ll)
kk = os.path.abspath(os.path.dirname('../test'))
print(kk)
