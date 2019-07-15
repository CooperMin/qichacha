#! /usr/bin/env python3
# -*- coding:utf-8 -*-
"""
调用mysql服务，执行插入/更新/查询操作
"""
import time
import pymysql

class ConnMysql():
    def __init__(self): #
        ## -- cedata服务器 -- ##
        # self.conn = pymysql.connect(
        #     host = 'dev.xiyiqq.com',
        #     port = 51306,
        #     user = 'cedata',
        #     passwd = 'xiyiDATA.1',
        #     db = 'cebd_laoshan'
        # )
        ## -- cedata服务器 -- ##

        ## -- 本地服务器 -- ##
        self.conn = pymysql.connect(
            host = 'localhost',
            port = 3306,
            user = 'root',
            passwd = 'admin',
            db = 'cebd_laoshan'
        )
        ## -- 本地服务器 -- ##

        self.cur = self.conn.cursor()

    def inssts(self,ins): #插入操作
        db = ConnMysql()
        try:
            db.cur.execute(ins)
            db.conn.commit()
            db.close()
            print('数据插入成功！')
        except Exception as e:
            db.conn.rollback()
            db.close()
            print(e)
            print('\n{0}\n{1}数据插入失败!{1}\n{0}'.format('*'*21,'*'*5))
            time.sleep(5)

    def updsts(self,upd): #更新操作
        db = ConnMysql()
        try:
            db.cur.execute(upd)
            db.conn.commit()
            db.close()
            print('\n数据更新成功！')
        except Exception as e:
            db.conn.rollback()
            db.close()
            print(e)
            print('\n{0}\n{1}数据更新失败!{1}\n{0}'.format('*'*21,'*'*5))

    def selsts(self,sel): #查询操作
        db = ConnMysql()
        try:
            db.cur.execute(sel)
            result = db.cur.fetchall()
            db.close()
        except Exception as e:
            db.conn.rollback()
            db.close()
            print(e)
            print('\n{0}\n{1}数据查询失败!{1}\n{0}'.format('*'*21,'*'*5))
            result = None
        return result


    def close(self): #关闭连接
        db = ConnMysql()
        db.conn.close()