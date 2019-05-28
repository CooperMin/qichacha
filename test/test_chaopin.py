#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import time
import random
import requests

from support.others import DealKey as dk
from support.headers import GeneralHeaders as gh

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
for num in range(1,260):
    num = str(num)
    if int(num) <10:
        num = '20000'+num
    elif int(num) <100:
        num = '2000'+num
    else:
        num = '200'+num
    print(num)
