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




