# to run this test: python3 -m testtools.run ceshi.py
# -*- coding: utf-8 -*-
import sys
sys.path.append('/Users/bixin/PycharmProjects/untitled1')
import unittest
import json
from unit.interface.api import BixinClient
from unit.HTMLTestRunner import HTMLTestRunner
import time

class BixinTestCase(unittest.TestCase):

    def setUp(self):
        super(BixinTestCase, self).setUp()
        # 小程序token
        cookies_file = "csrftoken=bktEoBhhC4xZxivsO8uv1qBZtqJJiPg902MDgkQ3kIS4f39jXsUy05wTr8PsErfs; bixin_session_id=mi3e7te3gztbejwuku0o94jxdzwty1sa; djlanguage=zh-Hans; browser=oqvId-2IAlB3SQQULjbYUw"  # cookies 文件路径
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1OTQ1MjEwMTksIm5vbmNlIjo3ODUzNjM5MDExNDg1NDAxNzgxLCJvcGVuaWQiOiIwZGQxODdhYjcxOGI0ZjJhODU0ZTdkZTMxNjEzNWUyYyJ9.knhaz9LKx-cGQHQMJ6_6rQ9IAWTpqxGYZ2SMi0TEMkI"  # CRFS token
        targetId = "0dd187ab718b4f2a854e7de316135e2c"  # targetId
        UA = "bixin-ios/2020070303 (iPhone; iOS 13.5.1; Scale/2.00; com.bixin.bixinasdev; asdev; UUID/81A9B3E9-3507-4D9B-89EB-A961C1EDE82D; Version/3.8.12; DeviceModel/iPhone11,8; SystemVersion/13.5.1)"
        Content_Type = "application/json"

        self.client_A = BixinClient(cookies_file, token, targetId, UA, Content_Type)

        # 客户端token
        token_app = "e1cc71af1f1646e0abb2ddcfa0f2f994"  # CRFS token
        targetId_app = ""
        Content_Type_app = "application/x-www-form-urlencoded"
        self.client_App = BixinClient(cookies_file, token_app, targetId_app, UA, Content_Type_app)

    def test_insure_user(self):
        '''
        访问用户信息接口
        :return:
        '''
        res = self.client_A.insure_user()
        self.assertEqual(200, res.status_code)  # 获取用户信息"接口状态码"

    def test_insure_assert(self):
        '''
        查询资产
        :return:
        '''
        currency = "BTC"
        assert_res = self.client_A.insure_assert(currency)
        self.assertEqual(200, assert_res.status_code)

    def test_INVALID_orderlist(self):
        '''
        查询orderlist类型：失效
        :return:
        '''
        status = "INVALID"
        page = 1
        page_size = 10
        orderlist = self.client_A.insure_orderlist(status, page, page_size)
        self.assertEqual(200, orderlist.status_code)
        order_status = json.loads(orderlist.content)["data"]["mapp_insure_order_list"]["order_list"][0]["status"]
        self.assertEqual("INVALID", order_status)

    def test_PEIDING_orderlist(self):
        '''
        查询orderlist类型：进行中
        :return:
        '''
        status = "INVALID"
        page = 1
        page_size = 10
        orderlist = self.client_A.insure_orderlist(status, page, page_size)
        self.assertEqual(200, orderlist.status_code)

    def test_PAID_orderlist(self):
        '''
        查询orderlist类型：  已支付
        :return:
        '''
        status = "PAID"
        page = 1
        page_size = 10
        orderlist = self.client_A.insure_orderlist(status, page, page_size)
        self.assertEqual(200, orderlist.status_code)
        order_status = json.loads(orderlist.content)["data"]["mapp_insure_order_list"]["order_list"][0]["status"]
        self.assertEqual("PAID", order_status)

    def test_insure_orderdetail(self):
        '''
        查询"失效"订单详情页
        :return:
        '''
        # 查询"失效"订单列表
        status = "INVALID"
        page = 1
        page_size = 10
        orderlist = self.client_A.insure_orderlist(status, page, page_size)
        self.assertEqual(200, orderlist.status_code)
        order_list = json.loads(orderlist.content)["data"]["mapp_insure_order_list"]["order_list"]
        # 查询列表"第一个"订单
        uuid = order_list[0]
        orderlist = self.client_A.insure_orderdetail(uuid)
        self.assertEqual(200, orderlist.status_code)


if __name__ == '__main__':
    # 创建测试集
    suit = unittest.TestSuite()
    suit.addTest(BixinTestCase('test_insure_orderdetail'))

    # 获取当前时间并指定时间格式
    now = time.strftime("%Y-%m-%d_%H_%M_%S")
    # 创建报告文件
    # fp = open(REPORT_PATH + now + "_report.html", 'wb')
    fp = open('/Users/bixin/PycharmProjects/untitled1/unit/report/' + "_report_all.html", 'wb')
    runner = HTMLTestRunner(stream=fp, title=u'接口自动化测试报告')
    runner.run(suit)
    fp.close()