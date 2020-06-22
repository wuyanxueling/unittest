# to run this test: python3 -m testtools.run test_baoxian.py
# -*- coding: utf-8 -*-
from testtools import TestCase
import requests
import json
import re



class BixinClient(object):

    def __init__(self, cookies_file, token, targetId):
        self.session = requests.Session()
        self.headers = {
            'Cookie': cookies_file,
            'Content-Type': 'application/json',
            'TargetId': targetId,
            'X-Access-Token': token
        }
        self.url_prefix = "https://sandboximb8.bixin.com/insure/graphql/graphql/"

    def insure_assert(self):
        '''
        获取保险用户资产
        :return:
        '''
        Mutation = '{\n          mapp_insure_user_c3_info {\n            is_c3_verified\n            nickname\n            icon\n            code\n          }\n        }'
        payload_query = {'query': Mutation}
        insure_user = requests.post(self.url_prefix, headers=self.headers, data=json.dumps(payload_query))
        return insure_user

    def insure_user(self):
        '''
        获取保险用户信息
        '''
        Mutation = '{\n          mapp_insure_user_c3_info {\n            is_c3_verified\n            nickname\n            icon\n            code\n          }\n        }'
        payload_query = {'query': Mutation}
        insure_user = requests.post(self.url_prefix, headers=self.headers, data=json.dumps(payload_query))
        return insure_user

    def insure_config(self):
        '''
        获取保险配置
        :return:
        '''
        Mutation = '''{\n       mapp_insure_symbol_info {\n         name,\n         symbol,\n         min_digits,\n         max_amount,\n         min_amount,\n         fee_rate,\n         period_list {\n           period,\n           puuid\n         }\n         insure_type\n         fee_amount\n         fee_amount_currency\n       }\n  }'''
        payload_query = {'query': Mutation}
        insure_config = requests.post(self.url_prefix, headers=self.headers, data=json.dumps(payload_query))
        return insure_config

    def insure_config_info(self):
        '''
         获取保险配置详细信息
         :return:
         '''
        Mutation = '''{\n       mapp_insure_config_info {\n         name,\n         symbol,\n         min_digits,\n         max_amount,\n         min_amount,\n         fee_rate,\n         period_list {\n           period,\n           puuid\n         }\n         insure_type\n         fee_amount\n         fee_amount_currency\n       }\n  }'''
        payload_query = {'query': Mutation}
        insure_config = requests.post(self.url_prefix, headers=self.headers, data=json.dumps(payload_query))
        return insure_config


    def insure_price(self, puuid, symbol, insure_type):
        '''
        获取实时价格接口
        :param puuid: 周期标识
        :param symbol: 交易对
        :param insure_type: 保险类型
        :return:
        '''

        Mutation = '''{\n          mapp_insure_exchange_price(puuid: "%s", symbol: "%s", insure_type: "%s") {\n            price\n            fee_rate\n            unit\n            period\n            limit_rate\n          }\n        }''' %(puuid, symbol, insure_type)
        payload_query = {'query': Mutation}
        insure_price = requests.post(self.url_prefix, headers=self.headers, data=json.dumps(payload_query))
        return insure_price

    def insure_pre_creat(self, insure_name, symbol, insured_price, insured_count, insured_period, insure_fee, insure_amount, insure_type, quote_amount, puuid, limit_rate, price_period):
        '''
        预创建接口
        :param insure_name: 保险名称
        :param symbol: 保险交易对
        :param insured_price: 保险价格
        :param insured_count: 保险数量
        :param insured_period: 保险周期
        :param insure_fee: 保险费率
        :param insure_amount: 保险费
        :param insure_type: 保险类型
        :param quote_amount: 保险折算金额
        :param puuid: 保险周期标识
        :param limit_rate: 保险费率
        :param price_period: 价格标识
        :return: 返回请求
        '''

        Mutation = '''mutation{\n              mapp_insure_pre_create_order(\n                insure_name: "%s",\n                symbol: "%s",\n                insured_price: "%s",\n                insured_count: "%s",\n                insured_period: %s,\n                insure_amount: "%s"\n                insure_fee: "%s"\n                insure_type: "%s"\n                quote_amount: "%s"\n                puuid: "%s"\n                limit_rate: "%s"\n                code: \"\",\n                source: \"\",\n                price_period: %s\n              ) {\n                deposit_order_id\n                currency\n                amount\n                address\n                memo\n              }\n            
            }'''%(insure_name, symbol, insured_price, insured_count, insured_period, insure_amount,insure_fee,  insure_type, quote_amount, puuid, limit_rate, price_period)
        print(Mutation)
        payload_query = {'query': Mutation}
        insure_creat = requests.post(self.url_prefix, headers=self.headers, data=json.dumps(payload_query))
        return insure_creat

    def insure_pay(self, target_address, amount, currency):
        '''
        支付
        :param target_address:
        :param amount:
        :param currency:
        :return:
        '''
        url = "https://sandboximb7.bixin.com/messenger/api/v3/transfer.create"
        payload_query = {"target_address": target_address, "amount": amount, "currency": currency}
        insure_pay = requests.post(url, headers=self.headers, data=json.dumps(payload_query))
        return insure_pay

    def insure_creat(self, deposit_order_id, puuid, unit, period):
        '''
        创建保险订单
        :param deposit_order_id: 充值订单ID
        :param puuid: 周期标识
        :param unit: 单位标识
        :param period: 时间标识
        :return:
        '''
        Mutation = '''mutation {
                        mapp_insure_create_order(deposit_order_id: "%s",puuid:'%s',unit:"%s",period:"%s") {
                            ok
                            err_msg
                            err_code
                            order_id
                        }
                    }'''%(deposit_order_id, puuid, unit, period)
        print(Mutation)
        payload_query = {'query': Mutation}
        insure_creat = requests.post(self.url_prefix, headers=self.headers, data=json.dumps(payload_query))
        return insure_creat

    def insure_orderlist(self, status, page, page_size):
        '''
        订单列表
        :param status:
        :param page:
        :param page_size:
        :return:
        '''
        Mutation = '''{\n        mapp_insure_order_list(\n          status: "%s",\n          page: %s,\n          page_size: %s,\n        ){\n          total_pages\n          order_list{\n            uuid\n            expire_at\n            amount\n            paid_amount\n            paid_amount_currency\n            insure_price_currency\n            insure_period\n            insure_price\n            status\n            insure_type\n          }\n        }\n      }
            ''' % (status, page, page_size)
        payload_query = {'query': Mutation}
        insure_list= requests.post(self.url_prefix, headers=self.headers, data=json.dumps(payload_query))
        return insure_list

    def insure_orderdetail(self, uuid):
        '''
        order详情页
        :param uuid:
        :return:
        '''
        Mutation = '''{\n        mapp_insure_order_info(uuid: "%s"){\n          confid_uuid\n          uuid\n          created_at\n          updated_at\n          expire_at\n          expire_price\n          insure_type\n          amount\n          amount_currency\n          quote_amount\n          insure_name\n          current_price\n          paid_amount\n          paid_amount_currency\n          expire_price_currency\n          current_price_currency\n          insure_amount_currency\n          insure_price_currency\n          insure_period\n          insure_amount\n          insure_price\n          status\n          paid_quote_amount\n          paid_quote_amount_currency\n        }\n      }''' % uuid
        payload_query = {'query': Mutation}
        insure_detail = requests.post(self.url_prefix, headers=self.headers, data=json.dumps(payload_query))
        return insure_detail




class BixinTestCase(TestCase):

    def setUp(self):
        super(BixinTestCase, self).setUp()
        cookies_file= "bixin_session_id=959pppejhdehrpwhikxyoj9aqo7qxlpu; djlanguage=zh-hans; csrftoken=ZgiVdRsFT4i0EUVkAv8rQQNo7TMRBiQAi6OpfY0U5th0oDqWuJJxY2cnnK1Wo96S; browser=A7C3zlPQPRil5Yke3VP8IQ"  # cookies 文件路径
        token= "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1OTI5NzE2NjgsIm5vbmNlIjo0NzI0ODc1NTQzOTA4MzQ0MzI0LCJvcGVuaWQiOiJjOGEyNmRlNmY4NTA0YWIzYTU5YTFkMTM3ZDZmNTlhNSJ9.Un0ueTIkI5JPf9d5VDPpaZbFcRUG13JJR0wsXtLC6Zo"  # CRFS token
        targetId= "8a26de6f8504ab3a59a1d137d6f59a5"  # targetId

        self.client_A = BixinClient(cookies_file, token, targetId)

    def test_insure_user(self):
        '''
        case1：访问用户信息接口
        :return:
        '''
        res = self.client_A.insure_user()
        self.assertEqual(200, res.status_code)  # 获取用户信息"接口状态码"


    def test_insure_price(self):
        '''
        case2:获取实时保险价格和费率
        :return:
        '''
        puuid = "8"
        symbol = "BTC/USDS"
        insure_type = "BTC_USDS_UP"
        res = self.client_A.insure_price(puuid, symbol, insure_type)
        self.assertEqual(200, res.status_code)  # 获取实时保险价格和费率"接口状态码"
        price_payload = json.loads(res.content)["data"]["mapp_insure_exchange_price"]["price"]
        print(price_payload)
        self.assertNotEqual("", price_payload)  #判断接口返回 不等于空值


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

        #第1步 获取保险配置信息
        config_res = self.client_A.insure_config()
        self.assertEqual(200, config_res.status_code)  # 判断获取保险配置"接口状态码"
        config_payload = json.loads(config_res.content)["data"]["mapp_insure_symbol_info"]

        #第2步 获取相关价格
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
        limit_rate = price_payload["fee_rate"]
        price_period = price_payload["period"]
        # 请求"预创建"接口值
        pre_res = self.client_A.insure_pre_creat(insure_name, symbol, insured_price, insured_count, insured_period, insure_fee, insure_amount, insure_type, quote_amount, puuid, limit_rate, price_period)
        self.assertEqual(200, pre_res.status_code)  # 判断接口正常
        amount = json.loads(pre_res.content)["data"]["mapp_insure_pre_create_order"]["amount"]
        print(amount)
        self.assertEqual(float(insure_amount), float(amount)) # 断点-判断保险数量与支付数量是否一致

    def test_insure_creat_case2(self):
        '''
        预创建接口（边界值测试）："小于"最小边界值
        :return:
        '''
        #第1步 获取保险配置信息
        config_res = self.client_A.insure_config()
        self.assertEqual(200, config_res.status_code)  # 判断获取保险配置"接口状态码"
        config_payload = json.loads(config_res.content)["data"]["mapp_insure_symbol_info"]

        #第2步 获取相关价格
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
        insured_count = "0。0000001"
        insured_period = config_payload[0]["period_list"][0]["period"]
        insure_fee = price_payload["fee_rate"]
        insure_amount = float(insured_count) * float(insure_fee)
        insure_type = config_payload[0]["insure_type"]
        a = float(insure_amount) * float(insured_price)
        quote_amount = str(a).split('.')[0] + '.' + str(a).split('.')[1][:2]
        puuid = config_payload[0]["period_list"][0]["puuid"]
        limit_rate = price_payload["fee_rate"]
        price_period = price_payload["period"]

        # 请求"预创建"接口值
        pre_res = self.client_A.insure_pre_creat(insure_name, symbol, insured_price, insured_count, insured_period, insure_fee, insure_amount, insure_type, quote_amount, puuid, limit_rate, price_period)
        self.assertEqual(200, pre_res.status_code)  # 判断接口正常
        error = json.loads(pre_res.content)["errors"][0]["code"]
        print(error)
        self.assertEqual(90007, error)  # 断点-判断返回错误码

    def test_insure_creat_case3(self):
        '''
        预创建接口（边界值测试）："等于"边界值
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
        insured_count = config_payload[0]["max_amount"]
        insured_period = config_payload[0]["period_list"][0]["period"]
        insure_fee = price_payload["fee_rate"]
        insure_amount = float(insured_count) * float(insure_fee)
        insure_type = config_payload[0]["insure_type"]
        a = float(insure_amount) * float(insured_price)
        quote_amount = str(a).split('.')[0] + '.' + str(a).split('.')[1][:2]
        puuid = config_payload[0]["period_list"][0]["puuid"]
        limit_rate = price_payload["fee_rate"]
        price_period = price_payload["period"]
        # 请求"预创建"接口值
        pre_res = self.client_A.insure_pre_creat(insure_name, symbol, insured_price, insured_count, insured_period,
                                                 insure_fee, insure_amount, insure_type, quote_amount, puuid,
                                                 limit_rate, price_period)
        self.assertEqual(200, pre_res.status_code)  # 判断pre预创建接口请求是否正常
        print(pre_res.content)
        self.assertEqual(float(insure_amount), float(
            json.loads(pre_res.content)["data"]["mapp_insure_pre_create_order"]["amount"]))  # 断点-判断保险数量与支付数量是否一致

    def test_insure_creat_case4(self):
        '''
        预创建接口（边界值测试）："大于"最大边界值
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
        insured_count = "20000000"
        insured_period = config_payload[0]["period_list"][0]["period"]
        insure_fee = price_payload["fee_rate"]
        insure_amount = float(insured_count) * float(insure_fee)
        insure_type = config_payload[0]["insure_type"]
        a = float(insure_amount) * float(insured_price)
        quote_amount = str(a).split('.')[0] + '.' + str(a).split('.')[1][:2]
        puuid = config_payload[0]["period_list"][0]["puuid"]
        limit_rate = price_payload["fee_rate"]
        price_period = price_payload["period"]
        # 请求"预创建"接口值
        pre_res = self.client_A.insure_pre_creat(insure_name, symbol, insured_price, insured_count, insured_period, insure_fee, insure_amount, insure_type, quote_amount, puuid, limit_rate, price_period)
        self.assertEqual(200, pre_res.status_code)  # 判断预创建接口正常
        error = json.loads(pre_res.content)["errors"][0]["code"]
        print(error)
        self.assertEqual(90006, error)  # 断点-判断返回错误码

    def test_insure_creat_case5(self):
        '''
        预创建接口（保险金额负值）：保险数量是负数
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
        insured_count = "-1"
        insured_period = config_payload[0]["period_list"][0]["period"]
        insure_fee = price_payload["fee_rate"]

        insure_amount = float(insured_count) * float(insure_fee)
        insure_type = config_payload[0]["insure_type"]
        a = float(insure_amount) * float(insured_price)
        quote_amount = str(a).split('.')[0] + '.' + str(a).split('.')[1][:2]
        puuid = config_payload[0]["period_list"][0]["puuid"]
        limit_rate = price_payload["fee_rate"]
        price_period = price_payload["period"]
        # 请求"预创建"接口值
        pre_res = self.client_A.insure_pre_creat(insure_name, symbol, insured_price, insured_count, insured_period,
                                                 insure_fee, insure_amount, insure_type, quote_amount, puuid,
                                                 limit_rate, price_period)
        self.assertEqual(200, pre_res.status_code)  # 判断接口正常
        error = json.loads(pre_res.content)["errors"][0]["code"]
        print(error)
        self.assertEqual(90006, error)  # 断点-保险数量是负数，判断返回错误码

    def test_insure_creat_case6(self):
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
        quote_amount = a # 不处理小数位数
        puuid = config_payload[0]["period_list"][0]["puuid"]
        limit_rate = price_payload["fee_rate"]
        price_period = price_payload["period"]

        # 请求"预创建"接口值
        pre_res = self.client_A.insure_pre_creat(insure_name, symbol, insured_price, insured_count, insured_period,
                                                 insure_fee, insure_amount, insure_type, quote_amount, puuid,
                                                 limit_rate, price_period)
        self.assertEqual(200, pre_res.status_code)  # 判断接口正常
        error_code= json.loads(pre_res.content)["errors"][0]["code"]
        self.assertEqual(90008, error_code)  # 断点-判断返回错误码

    def test_insure_creat_case7(self):
        '''
        预创建接口：交易对利率周期不存在 = "90001"
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
        insured_period = "12233" # 任意输入值/或者为：空
        insure_fee = price_payload["fee_rate"]
        insure_amount = float(insured_count) * float(insure_fee)
        insure_type = config_payload[0]["insure_type"]
        a = float(insure_amount) * float(insured_price)
        quote_amount = str(a).split('.')[0] + '.' + str(a).split('.')[1][:2]  # 不处理小数位数
        puuid = config_payload[0]["period_list"][0]["puuid"]
        limit_rate = price_payload["fee_rate"]
        price_period = price_payload["period"]

        # 请求"预创建"接口值
        pre_res = self.client_A.insure_pre_creat(insure_name, symbol, insured_price, insured_count, insured_period,
                                                 insure_fee, insure_amount, insure_type, quote_amount, puuid,
                                                 limit_rate, price_period)
        self.assertEqual(200, pre_res.status_code)  # 判断接口正常
        error_code = json.loads(pre_res.content)["errors"][0]["code"]
        self.assertEqual(90001, error_code)  # 断点-判断返回错误码

    def test_insure_creat_case8(self):
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
        insure_amount = "89"        #任意数值/或者为空
        insure_type = config_payload[0]["insure_type"]
        a = float(insure_amount) * float(insured_price)
        quote_amount = str(a).split('.')[0] + '.' + str(a).split('.')[1][:2]
        puuid = config_payload[0]["period_list"][0]["puuid"]
        limit_rate = price_payload["fee_rate"]
        price_period = price_payload["period"]

        # 请求"预创建"接口值
        pre_res = self.client_A.insure_pre_creat(insure_name, symbol, insured_price, insured_count, insured_period,
                                                 insure_fee, insure_amount, insure_type, quote_amount, puuid,
                                                 limit_rate, price_period)
        self.assertEqual(200, pre_res.status_code)  # 判断接口正常
        error_code = json.loads(pre_res.content)["errors"][0]["code"]
        self.assertEqual(90007, error_code)  # 断点-判断返回错误码

    def test_insure_creat_case9(self):
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
        insure_fee = "20"           #任意数值
        insure_amount = float(insured_count) * float(insure_fee)
        insure_type = config_payload[0]["insure_type"]
        a = float(insure_amount) * float(insured_price)
        quote_amount = str(a).split('.')[0] + '.' + str(a).split('.')[1][:2]
        puuid = config_payload[0]["period_list"][0]["puuid"]
        limit_rate = price_payload["fee_rate"]
        price_period = price_payload["period"]

        # 请求"预创建"接口值
        pre_res = self.client_A.insure_pre_creat(insure_name, symbol, insured_price, insured_count, insured_period,
                                                 insure_fee, insure_amount, insure_type, quote_amount, puuid,
                                                 limit_rate, price_period)
        self.assertEqual(200, pre_res.status_code)  # 判断接口正常
        error_code = json.loads(pre_res.content)["errors"][0]["code"]
        self.assertEqual(90001, error_code)  # 断点-判断返回错误码


    def test_insure_orderlist(self):
        '''
        查询orderlist
        :return:
        '''
        status = "SAFING"
        page = 1
        page_size = 10
        orderlist = self.client_A.insure_orderlist( status, page, page_size)
        self.assertEqual(200,orderlist.content)

    def test_insure_orderdetail(self):
        '''
        查询订单详情页
        :return:
        '''
        status = "SAFING"
        page = 1
        page_size = 10
        orderlist = self.client_A.insure_orderlist( status, page, page_size)
        self.assertEqual(200,orderlist.content)
        order_uuid =json.loads(orderlist.content)["data"]["order_list"][0]
        if order_uuid is not None:
            uuid = order_uuid
            orderlist = self.client_A.insure_orderdetail(uuid)
            self.assertEqual(200, orderlist.content)

