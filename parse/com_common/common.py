#! /usr/bin/env python3
from lxml import etree

from support.mysql import QccMysql as db

class GeneralMethod():
    def __init__(self):
        self.db = db()

    def upd_status(self, com_id,status_column,count_column, count):  # 更新com_info表相关字段状态码
        if count == -1: #表示页面无此内容
            status = -1
        elif count == 0: #表示数据量为0
            status = 0
        else:
            status = 9 #此状态表示有数据但未采集
        upd = f"""
            UPDATE 
            `com_info` 
            SET
            `{status_column}` = "{status}",`{count_column}` = "{count}"
            WHERE 
            `com_id` = "{com_id}" ;
            """
        self.db.updsts(upd)

    def verify(self,res): #判断网站访问是否需要验证，若可正常访问则返回结果树
        global tree
        if '<script>window.location.href' in res:
            print('访问频繁，需验证！{rc_judge}')
            input('暂停')
        elif '<script>location.href="/user_login"</script>' in res:
            print('Cookie失效，需更换！{rc_judge}')
            input('程序暂停运行！')
        elif '您的账号访问超频，请稍后访问或联系客服人员' in res:
            print('账号访问超频，请更换账号！{rc_judge}')
            input('程序暂停运行！')
        else:
            tree = etree.HTML(res)
        return tree
