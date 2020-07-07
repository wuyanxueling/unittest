# to run this test: python3 -m testtools.run test_case.py
# -*- coding: utf-8 -*-
import unittest
import json
import sys
sys.path.append('/Users/bixin/PycharmProjects/untitled1')
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

    def test_insure_price(self):
        '''
        获取实时保险价格和费率
        :return:
        '''
        puuid = "8"
        symbol = "BTC/USDS"
        insure_type = "BTC_USDS_UP"
        res = self.client_A.insure_price(puuid, symbol, insure_type)
        self.assertEqual(200, res.status_code)  # 获取实时保险价格和费率"接口状态码"
        price_payload = json.loads(res.content)["data"]["mapp_insure_exchange_price"]["price"]
        print(price_payload)
        self.assertNotEqual("", price_payload)  # 判断接口返回 不等于空值

    def test_insure_config(self):
        '''
        获取保险配置
        :return:
        '''
        res = self.client_A.insure_config()
        self.assertEqual(200, res.status_code)  # 判断获取保险配置"接口状态码"
        print(res.content)

    def test_insure_creat_case1(self):
        '''
        预创建订单-正常创建
        :return:
        '''

        # 第1步 获取保险配置信息
        config_res = self.client_A.insure_config()
        self.assertEqual(200, config_res.status_code)  # 判断获取保险配置"接口状态码"
        config_payload = json.loads(config_res.content)["data"]["mapp_insure_symbol_info"]

        # 第2步 获取相关价格
        # 设置"实时价格"参数配置
        puuid = config_payload[0]["period_list"][0]["puuid"]
        symbol = config_payload[0]["symbol"]
        insure_type = config_payload[0]["insure_type"]
        # 查询实时价格
        price_res = self.client_A.insure_price(puuid, symbol, insure_type)
        self.assertEqual(200, price_res.status_code)  # 判断实时价格是否正确
        price_payload = json.loads(price_res.content)["data"]["mapp_insure_exchange_price"]

        # 设置"预创建"参数设置
        insure_name = config_payload[0]["name"]
        insured_price = price_payload["price"]
        insured_count = "1"
        insured_period = config_payload[0]["period_list"][0]["period"]
        insure_fee = price_payload["fee_rate"]
        insure_amount = float(insured_count) * float(insure_fee)
        insure_type = config_payload[0]["insure_type"]
        a = float(insure_amount) * float(insured_price)
        quote_amount = str(a).split('.')[0] + '.' + str(a).split('.')[1][:2]
        puuid = config_payload[0]["period_list"][0]["puuid"]
        limit_rate = price_payload["limit_rate"]
        price_period = price_payload["period"]
        # 请求"预创建"接口值
        pre_res = self.client_A.insure_pre_creat(insure_name, symbol, insured_price, insured_count, insured_period,
                                                 insure_fee, insure_amount, insure_type, quote_amount, puuid,
                                                 limit_rate, price_period)
        self.assertEqual(200, pre_res.status_code)  # 判断接口正常
        amount = json.loads(pre_res.content)["data"]["mapp_insure_pre_create_order"]["amount"]
        print(amount)
        self.assertEqual(float(insure_amount), float(amount))  # 断点-判断保险数量与支付数量是否一致

    def test_insure_creat_case2(self):
        '''
        预创建接口（边界值测试）："小于"最小边界值
        :return: 返回错误码：90022
        '''
        # 第1步 获取保险配置信息
        config_res = self.client_A.insure_config()
        self.assertEqual(200, config_res.status_code)  # 判断获取保险配置"接口状态码"
        config_payload = json.loads(config_res.content)["data"]["mapp_insure_symbol_info"]

        # 第2步 获取相关价格
        # 设置"实时价格"参数配置
        puuid = config_payload[0]["period_list"][0]["puuid"]
        symbol = config_payload[0]["symbol"]
        insure_type = config_payload[0]["insure_type"]
        # 查询实时价格
        price_res = self.client_A.insure_price(puuid, symbol, insure_type)
        self.assertEqual(200, price_res.status_code)  # 判断实时价格是否正确
        price_payload = json.loads(price_res.content)["data"]["mapp_insure_exchange_price"]

        # 设置"预创建"参数设置
        insure_name = config_payload[0]["name"]
        insured_price = price_payload["price"]
        insured_count = "0.000001"
        insured_period = config_payload[0]["period_list"][0]["period"]
        insure_fee = price_payload["fee_rate"]
        insure_amount = float(insured_count) * float(insure_fee)
        insure_type = config_payload[0]["insure_type"]
        a = float(insure_amount) * float(insured_price)
        quote_amount = str(a).split('.')[0] + '.' + str(a).split('.')[1][:2]
        puuid = config_payload[0]["period_list"][0]["puuid"]
        limit_rate = price_payload["limit_rate"]
        price_period = price_payload["period"]

        # 请求"预创建"接口值
        pre_res = self.client_A.insure_pre_creat(insure_name, symbol, insured_price, insured_count, insured_period,
                                                 insure_fee, insure_amount, insure_type, quote_amount, puuid,
                                                 limit_rate, price_period)
        self.assertEqual(200, pre_res.status_code)  # 判断接口正常
        error = json.loads(pre_res.content)["errors"][0]["code"]
        print(error)
        self.assertEqual(90022, error)  # 断点-判断返回错误码：？？

    '''
    def test_insure_creat_case3(self):

        预创建接口（边界值测试）："等于"边界值（config边界值接口没有直接返回）
        :return:

        # 第1步 获取保险配置信息
        config_res = self.client_A.insure_config()
        self.assertEqual(200, config_res.status_code)  # 判断获取保险配置"接口状态码"
        config_payload = json.loads(config_res.content)["data"]["mapp_insure_symbol_info"]

        # 第2步 获取相关价格
        # 设置"实时价格"参数配置
        puuid = config_payload[0]["period_list"][0]["puuid"]
        symbol = config_payload[0]["symbol"]
        insure_type = config_payload[0]["insure_type"]
        # 查询实时价格
        price_res = self.client_A.insure_price(puuid, symbol, insure_type)
        self.assertEqual(200, price_res.status_code)  # 判断实时价格是否正确
        price_payload = json.loads(price_res.content)["data"]["mapp_insure_exchange_price"]

        # 设置"预创建"参数设置
        insure_name = config_payload[0]["name"]
        insured_price = price_payload["price"]
        insured_count = config_payload[0]["max_amount"]
        insured_period = config_payload[0]["period_list"][0]["period"]
        insure_fee = price_payload["fee_rate"]
        insure_amount = float(insured_count) * float(insure_fee)
        insure_type = config_payload[0]["insure_type"]
        a = float(insure_amount) * float(insured_price)
        quote_amount = str(a).split('.')[0] + '.' + str(a).split('.')[1][:2]
        puuid = config_payload[0]["period_list"][0]["puuid"]
        limit_rate = price_payload["limit_rate"]
        price_period = price_payload["period"]
        # 请求"预创建"接口值
        pre_res = self.client_A.insure_pre_creat(insure_name, symbol, insured_price, insured_count, insured_period,
                                                 insure_fee, insure_amount, insure_type, quote_amount, puuid,
                                                 limit_rate, price_period)
        self.assertEqual(200, pre_res.status_code)  # 判断pre预创建接口请求是否正常
        print(pre_res.content)
        self.assertEqual(float(insure_amount), float(
            json.loads(pre_res.content)["data"]["mapp_insure_pre_create_order"]["amount"]))  # 断点-判断保险数量与支付数量是否一致
    '''

    def test_insure_creat_case3(self):
        '''
        预创建接口（边界值测试）："大于"最大边界值
        :return:返回错误码：90021（下单失败）
        '''

        # 第1步 获取保险配置信息
        config_res = self.client_A.insure_config()
        self.assertEqual(200, config_res.status_code)  # 判断获取保险配置"接口状态码"
        config_payload = json.loads(config_res.content)["data"]["mapp_insure_symbol_info"]

        # 第2步 获取相关价格
        # 设置"实时价格"参数配置
        puuid = config_payload[0]["period_list"][0]["puuid"]
        symbol = config_payload[0]["symbol"]
        insure_type = config_payload[0]["insure_type"]
        # 查询实时价格
        price_res = self.client_A.insure_price(puuid, symbol, insure_type)
        self.assertEqual(200, price_res.status_code)  # 判断实时价格是否正确
        price_payload = json.loads(price_res.content)["data"]["mapp_insure_exchange_price"]

        # 设置"预创建"参数设置
        insure_name = config_payload[0]["name"]
        insured_price = price_payload["price"]
        insured_count = "20000000"
        insured_period = config_payload[0]["period_list"][0]["period"]
        insure_fee = price_payload["fee_rate"]
        insure_amount = float(insured_count) * float(insure_fee)
        insure_type = config_payload[0]["insure_type"]
        a = float(insure_amount) * float(insured_price)
        quote_amount = str(a).split('.')[0] + '.' + str(a).split('.')[1][:2]
        puuid = config_payload[0]["period_list"][0]["puuid"]
        limit_rate = price_payload["limit_rate"]
        price_period = price_payload["period"]
        # 请求"预创建"接口值
        pre_res = self.client_A.insure_pre_creat(insure_name, symbol, insured_price, insured_count, insured_period,
                                                 insure_fee, insure_amount, insure_type, quote_amount, puuid,
                                                 limit_rate, price_period)
        self.assertEqual(200, pre_res.status_code)  # 判断预创建接口正常
        error = json.loads(pre_res.content)["errors"][0]["code"]
        self.assertEqual(90021, error)  # 断点-判断返回错误码，下单失败

    def test_insure_creat_case4(self):
        '''
        预创建接口（保险金额负值）：保险数量是负数
        :return: 返回错误码：90000
        '''

        # 第1步 获取保险配置信息
        config_res = self.client_A.insure_config()
        self.assertEqual(200, config_res.status_code)  # 判断获取保险配置"接口状态码"
        config_payload = json.loads(config_res.content)["data"]["mapp_insure_symbol_info"]

        # 第2步 获取相关价格
        # 设置"实时价格"参数配置
        puuid = config_payload[0]["period_list"][0]["puuid"]
        symbol = config_payload[0]["symbol"]
        insure_type = config_payload[0]["insure_type"]
        # 查询实时价格
        price_res = self.client_A.insure_price(puuid, symbol, insure_type)
        self.assertEqual(200, price_res.status_code)  # 判断实时价格是否正确
        price_payload = json.loads(price_res.content)["data"]["mapp_insure_exchange_price"]

        # 设置"预创建"参数设置
        insure_name = config_payload[0]["name"]
        insured_price = price_payload["price"]
        insured_count = "-1"
        insured_period = config_payload[0]["period_list"][0]["period"]
        insure_fee = price_payload["fee_rate"]

        insure_amount = float(insured_count) * float(insure_fee)
        insure_type = config_payload[0]["insure_type"]
        a = float(insure_amount) * float(insured_price)
        quote_amount = str(a).split('.')[0] + '.' + str(a).split('.')[1][:2]
        puuid = config_payload[0]["period_list"][0]["puuid"]
        limit_rate = price_payload["limit_rate"]
        price_period = price_payload["period"]
        # 请求"预创建"接口值
        pre_res = self.client_A.insure_pre_creat(insure_name, symbol, insured_price, insured_count, insured_period,
                                                 insure_fee, insure_amount, insure_type, quote_amount, puuid,
                                                 limit_rate, price_period)
        self.assertEqual(200, pre_res.status_code)  # 判断接口正常
        error = json.loads(pre_res.content)["errors"][0]["code"]
        self.assertEqual(90000, error)  # 断点-保险数量是负数，判断返回错误码

    def test_insure_creat_case5(self):
        '''
        预创建接口：折算金额错误，不处理折算金额小数位数
        :return:判断服务端验证折合金额错误 = "90008"
        '''

        # 第1步 获取保险配置信息
        config_res = self.client_A.insure_config()
        self.assertEqual(200, config_res.status_code)  # 判断获取保险配置"接口状态码"
        config_payload = json.loads(config_res.content)["data"]["mapp_insure_symbol_info"]

        # 第2步 获取相关价格
        # 设置"实时价格"参数配置
        puuid = config_payload[0]["period_list"][0]["puuid"]
        symbol = config_payload[0]["symbol"]
        insure_type = config_payload[0]["insure_type"]
        # 查询实时价格
        price_res = self.client_A.insure_price(puuid, symbol, insure_type)
        self.assertEqual(200, price_res.status_code)  # 判断实时价格是否正确
        price_payload = json.loads(price_res.content)["data"]["mapp_insure_exchange_price"]

        # 设置"预创建"参数设置
        insure_name = config_payload[0]["name"]
        insured_price = price_payload["price"]
        insured_count = "1"
        insured_period = config_payload[0]["period_list"][0]["period"]
        insure_fee = price_payload["fee_rate"]
        insure_amount = float(insured_count) * float(insure_fee)
        insure_type = config_payload[0]["insure_type"]
        a = float(insure_amount) * float(insured_price)
        quote_amount = a  # 不处理小数位数
        puuid = config_payload[0]["period_list"][0]["puuid"]
        limit_rate = price_payload["limit_rate"]
        price_period = price_payload["period"]

        # 请求"预创建"接口值
        pre_res = self.client_A.insure_pre_creat(insure_name, symbol, insured_price, insured_count, insured_period,
                                                 insure_fee, insure_amount, insure_type, quote_amount, puuid,
                                                 limit_rate, price_period)
        self.assertEqual(200, pre_res.status_code)  # 判断接口正常
        error_code = json.loads(pre_res.content)["errors"][0]["code"]
        self.assertEqual(90008, error_code)  # 断点-判断返回错误码

    def test_insure_creat_case6(self):
        '''
        预创建接口：交易对利率周期下架，不存在 = "90025"
        :return:
        '''
        # 第1步 获取保险配置信息
        config_res = self.client_A.insure_config()
        self.assertEqual(200, config_res.status_code)  # 判断获取保险配置"接口状态码"
        config_payload = json.loads(config_res.content)["data"]["mapp_insure_symbol_info"]

        # 第2步 获取相关价格
        # 设置"实时价格"参数配置
        puuid = config_payload[0]["period_list"][0]["puuid"]
        symbol = config_payload[0]["symbol"]
        insure_type = config_payload[0]["insure_type"]
        # 查询实时价格
        price_res = self.client_A.insure_price(puuid, symbol, insure_type)
        self.assertEqual(200, price_res.status_code)  # 判断实时价格是否正确
        price_payload = json.loads(price_res.content)["data"]["mapp_insure_exchange_price"]

        # 设置"预创建"参数设置
        insure_name = config_payload[0]["name"]
        insured_price = price_payload["price"]
        insured_count = "1"
        insured_period = "12233"  # 任意输入值/或者为：空
        insure_fee = price_payload["fee_rate"]
        insure_amount = float(insured_count) * float(insure_fee)
        insure_type = config_payload[0]["insure_type"]
        a = float(insure_amount) * float(insured_price)
        quote_amount = str(a).split('.')[0] + '.' + str(a).split('.')[1][:2]  # 不处理小数位数
        puuid = config_payload[0]["period_list"][0]["puuid"]
        limit_rate = price_payload["limit_rate"]
        price_period = price_payload["period"]

        # 请求"预创建"接口值
        pre_res = self.client_A.insure_pre_creat(insure_name, symbol, insured_price, insured_count, insured_period,
                                                 insure_fee, insure_amount, insure_type, quote_amount, puuid,
                                                 limit_rate, price_period)
        self.assertEqual(200, pre_res.status_code)  # 判断接口正常
        error_code = json.loads(pre_res.content)["errors"][0]["code"]
        self.assertEqual(90025, error_code)  # 断点-判断返回错误码

    def test_insure_creat_case7(self):
        '''
        预创建接口：服务端验证保险费错误 = "90007"
        :return:
        '''
        # 第1步 获取保险配置信息
        config_res = self.client_A.insure_config()
        self.assertEqual(200, config_res.status_code)  # 判断获取保险配置"接口状态码"
        config_payload = json.loads(config_res.content)["data"]["mapp_insure_symbol_info"]

        # 第2步 获取相关价格
        # 设置"实时价格"参数配置
        puuid = config_payload[0]["period_list"][0]["puuid"]
        symbol = config_payload[0]["symbol"]
        insure_type = config_payload[0]["insure_type"]
        # 查询实时价格
        price_res = self.client_A.insure_price(puuid, symbol, insure_type)
        self.assertEqual(200, price_res.status_code)  # 判断实时价格是否正确
        price_payload = json.loads(price_res.content)["data"]["mapp_insure_exchange_price"]

        # 设置"预创建"参数设置
        insure_name = config_payload[0]["name"]
        insured_price = price_payload["price"]
        insured_count = "1"
        insured_period = config_payload[0]["period_list"][0]["period"]
        insure_fee = price_payload["fee_rate"]
        insure_amount = "89"  # 任意数值/或者为空
        insure_type = config_payload[0]["insure_type"]
        a = float(insure_amount) * float(insured_price)
        quote_amount = str(a).split('.')[0] + '.' + str(a).split('.')[1][:2]
        puuid = config_payload[0]["period_list"][0]["puuid"]
        limit_rate = price_payload["limit_rate"]
        price_period = price_payload["period"]

        # 请求"预创建"接口值
        pre_res = self.client_A.insure_pre_creat(insure_name, symbol, insured_price, insured_count, insured_period,
                                                 insure_fee, insure_amount, insure_type, quote_amount, puuid,
                                                 limit_rate, price_period)
        self.assertEqual(200, pre_res.status_code)  # 判断接口正常
        error_code = json.loads(pre_res.content)["errors"][0]["code"]
        self.assertEqual(90007, error_code)  # 断点-判断返回错误码

    def test_insure_creat_case8(self):
        '''
        预创建接口：保险费率验证失败 = "90001"
        :return:
        '''

        # 第1步 获取保险配置信息
        config_res = self.client_A.insure_config()
        self.assertEqual(200, config_res.status_code)  # 判断获取保险配置"接口状态码"
        config_payload = json.loads(config_res.content)["data"]["mapp_insure_symbol_info"]

        # 第2步 获取相关价格
        # 设置"实时价格"参数配置
        puuid = config_payload[0]["period_list"][0]["puuid"]
        symbol = config_payload[0]["symbol"]
        insure_type = config_payload[0]["insure_type"]
        # 查询实时价格
        price_res = self.client_A.insure_price(puuid, symbol, insure_type)
        self.assertEqual(200, price_res.status_code)  # 判断实时价格是否正确
        price_payload = json.loads(price_res.content)["data"]["mapp_insure_exchange_price"]

        # 设置"预创建"参数设置
        insure_name = config_payload[0]["name"]
        insured_price = price_payload["price"]
        insured_count = "1"
        insured_period = config_payload[0]["period_list"][0]["period"]
        insure_fee = "20"  # 任意数值
        insure_amount = float(insured_count) * float(insure_fee)
        insure_type = config_payload[0]["insure_type"]
        a = float(insure_amount) * float(insured_price)
        quote_amount = str(a).split('.')[0] + '.' + str(a).split('.')[1][:2]
        puuid = config_payload[0]["period_list"][0]["puuid"]
        limit_rate = price_payload["limit_rate"]
        price_period = price_payload["period"]

        # 请求"预创建"接口值
        pre_res = self.client_A.insure_pre_creat(insure_name, symbol, insured_price, insured_count, insured_period,
                                                 insure_fee, insure_amount, insure_type, quote_amount, puuid,
                                                 limit_rate, price_period)
        self.assertEqual(200, pre_res.status_code)  # 判断接口正常
        error_code = json.loads(pre_res.content)["errors"][0]["code"]
        self.assertEqual(90001, error_code)  # 断点-判断返回错误码

    def test_create_ok(self):
        # 第1步 获取保险配置信息
        config_res = self.client_A.insure_config()
        self.assertEqual(200, config_res.status_code)  # 判断获取保险配置"接口状态码"
        config_payload = json.loads(config_res.content)["data"]["mapp_insure_symbol_info"]

        # 第2步 获取相关价格
        # 设置"实时价格"参数配置
        puuid = config_payload[1]["period_list"][0]["puuid"]
        symbol = config_payload[1]["symbol"]
        insure_type = config_payload[1]["insure_type"]
        # 查询实时价格
        price_res = self.client_A.insure_price(puuid, symbol, insure_type)
        self.assertEqual(200, price_res.status_code)  # 判断实时价格是否正确
        price_payload = json.loads(price_res.content)["data"]["mapp_insure_exchange_price"]

        # 设置"预创建"参数设置
        insure_name = config_payload[1]["name"]
        insured_price = price_payload["price"]
        insured_count = "1"
        insured_period = config_payload[1]["period_list"][0]["period"]
        insure_fee = price_payload["fee_rate"]
        insure_amount = float(insured_count) * float(insure_fee)
        insure_type = config_payload[1]["insure_type"]
        a = float(insure_amount) * float(insured_price)
        quote_amount = str(a).split('.')[0] + '.' + str(a).split('.')[1][:2]
        puuid = config_payload[1]["period_list"][0]["puuid"]
        limit_rate = price_payload["limit_rate"]
        price_period = price_payload["period"]
        # 请求"预创建"接口值
        pre_res = self.client_A.insure_pre_creat(insure_name, symbol, insured_price, insured_count, insured_period,
                                                 insure_fee, insure_amount, insure_type, quote_amount, puuid,
                                                 limit_rate, price_period)
        self.assertEqual(200, pre_res.status_code)  # 判断接口正常
        pre_result = json.loads(pre_res.content)["data"]["mapp_insure_pre_create_order"]

        # 支付信息接口
        message = "支付"
        title = "请输入密码"
        amount = pre_result["amount"]
        currency = pre_result["currency"]
        target_addr = pre_result["address"]
        order_id = pre_result["deposit_order_id"]
        request_id = pre_result["deposit_order_id"]
        payinfo_res = self.client_App.insure_payinfo(message, title, amount, currency, target_addr,
                                                     order_id, request_id)

        # 支付创建接口
        pay_amount = pre_result["amount"]
        payment_password = "123456"
        pay_request_id = pre_result["deposit_order_id"]
        pay_seq = json.loads(payinfo_res.content)["data"]["seq"]
        pay_res = self.client_App.insure_pay(message, pay_amount, payment_password, pay_request_id, pay_seq)

        # 预创建接口
        deposit_order_id = pre_result["deposit_order_id"]
        puuid = config_payload[1]["period_list"][0]["puuid"]
        unit = pre_result["currency"]
        period = price_payload["period"]
        create_res = self.client_A.insure_creat(deposit_order_id, puuid, unit, period)
        print(create_res.content)

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
        查询orderlist类型：
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