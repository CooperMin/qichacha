#! /usr/bin/env python3
# -*- coding:utf-8 -*-
from parse.com_expand.qcc_patent import PatentInfo as pt
from parse.com_expand.qcc_credit.qcc_credit_execued import Credit as ct
from parse.com_expand.qcc_credit.qcc_credit_breach_of_faith_execued import FaithExecued as fe
from parse.com_expand.qcc_recruit import RecruitInfo as rc

class StartApp():
    def running(self):
        rc().rc_info() #招聘
        # pt().run() #专利信息
        # ct().get_page_info() #被执行人
        # fe().get_page_info() #失信被执行人



if __name__ == '__main__':
    StartApp().running()




