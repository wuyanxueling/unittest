# to run this test: python3 -m testtools.run ceshi.py
# -*- coding: utf-8 -*-
import sys
sys.path.append('/Users/bixin/PycharmProjects/untitled1')
import unittest
# from unit.case.test_case import BixinTestCase
from unit.HTMLTestRunner import HTMLTestRunner
import time


if __name__ == '__main__':
    # 创建测试集
    '''
    suit = unittest.TestSuite()
    suit.addTest(BixinTestCase('test_insure_orderdetail'))
    '''
    TESTCASE_PATH = '/Users/bixin/PycharmProjects/untitled1/unit/case'
    suit = unittest.defaultTestLoader.discover(TESTCASE_PATH, pattern='test_*.py')


    # 获取当前时间并指定时间格式
    now = time.strftime("%Y-%m-%d_%H_%M_%S")
    # 创建报告文件
    # fp = open(REPORT_PATH + now + "_report.html", 'wb')
    fp = open('/Users/bixin/PycharmProjects/untitled1/unit/report/' + "_report_all.html", 'wb')
    runner = HTMLTestRunner(stream=fp, title=u'接口自动化测试报告')
    runner.run(suit)
    fp.close()