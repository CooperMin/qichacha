#! /usr/bin/env python3
# -*- coding:utf-8 -*-
"""
调用mysql服务，执行插入/更新/查询操作
"""

import pymysql
import time

class QccMysql():
    def __init__(self): #数据库连接信息
        # self.conn = pymysql.connect(
        #     host = 'dev.xiyiqq.com',
        #     port = 51306,
        #     user = 'cedata',
        #     passwd = 'xiyiDATA.1',
        #     db = 'cebd_laoshan'
        # )
        self.conn = pymysql.connect(
            host = 'localhost',
            port = 3306,
            user = 'root',
            passwd = 'admin',
            db = 'cebd_laoshan'
        )
        self.cur = self.conn.cursor()

    def inssts(self,ins): #插入操作
        try:
            self.cur.execute(ins)
            self.conn.commit()
            self.close()
            print('数据插入成功！')
        except Exception as e:
            self.conn.rollback()
            self.close()
            print(e)
            print('\n{0}\n{1}数据插入失败!{1}\n{0}'.format('*'*21,'*'*5))
            time.sleep(5)

    def updsts(self,upd): #更新操作
        try:
            # print(upd)
            self.cur.execute(upd)
            self.conn.commit()
            self.close()
            print('\n数据更新成功！')
        except Exception as e:
            self.conn.rollback()
            self.close()
            print(e)
            print('\n{0}\n{1}数据更新失败!{1}\n{0}'.format('*'*21,'*'*5))

    def selsts(self,sel): #查询操作
        try:
            self.cur.execute(sel)
            result = self.cur.fetchall()
            self.close()
        except Exception as e:
            self.conn.rollback()
            self.close()
            print(e)
            print('\n{0}\n{1}数据查询失败!{1}\n{0}'.format('*'*21,'*'*5))
            result = None
        return result


    def close(self): #关闭连接
        self.conn.close()



