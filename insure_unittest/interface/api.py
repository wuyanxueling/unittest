# to run this test: python3 -m testtools.run test_baoxian.py
# -*- coding: utf-8 -*-
import requests
import json
import urllib.parse
import urllib
import re

class BixinClient(object):

    def __init__(self, cookies_file, token, targetId, UA, Content_Type):
        self.session = requests.Session()
        self.headers = {
            'Cookie': cookies_file,
            'Content-Type': Content_Type,
            'TargetId': targetId,
            'User-Agent': UA,
            'X-Access-Token': token
        }
        self.url_prefix = "https://sandboximb8.bixin.com/insure/graphql/graphql/"

    def insure_assert(self, currency):
        '''
        获取保险用户资产
        :return:
        '''
        Mutation = '''query {
        mapp_insure_user_assert_info(currency:"%s"){
            amount,
            unit
         }
        }'''% currency
        payload_query = {'query': Mutation}
        insure_user = requests.post(self.url_prefix, headers=self.headers, data=json.dumps(payload_query))
        return insure_user

    def insure_user(self):
        '''
        获取保险用户信息
        '''
        Mutation = '''{
          mapp_insure_user_c3_info {
            is_c3_verified
            nickname
            icon
            code
            uid
          }
        }'''
        payload_query = {'query': Mutation}
        insure_user = requests.post(self.url_prefix, headers=self.headers, data=json.dumps(payload_query))
        return insure_user

    def insure_config(self):
        '''
        获取保险配置
        :return:
        '''
        Mutation = '''{
       mapp_insure_symbol_info {
         uuid,
         name,
         symbol,
         min_digits,
         max_amount,
         min_amount,
         fee_rate,
         period_list {
           period,
           puuid
         }
         insure_type
         fee_amount
         fee_amount_currency
         is_active
       }
  }'''
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

        Mutation = '''{
          mapp_insure_exchange_price(puuid: "%s", symbol: "%s", insure_type: "%s") {
            price
            fee_rate
            unit
            period
            limit_rate
          }
        }''' % (puuid, symbol, insure_type)

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
        Mutation = '''mutation {
              mapp_insure_pre_create_order(
                insure_name: "%s",
                symbol: "%s",
                insured_price: "%s",
                insured_count: "%s",
                insured_period: %s,
                insure_amount: "%s"
                insure_fee: "%s"
                insure_type: "%s"
                quote_amount: "%s"
                puuid: "%s"
                limit_rate: "%s"
                code: "",
                source: "",
                price_period: %s
              ) {
                deposit_order_id
                currency
                amount
                address
                memo
              }
            }''' % (insure_name, symbol, insured_price, insured_count, insured_period, insure_amount, insure_fee, insure_type, quote_amount, puuid, limit_rate, price_period)
        payload_query = {'query': Mutation}
        insure_creat = requests.post(self.url_prefix, headers=self.headers, data=json.dumps(payload_query))
        return insure_creat

    def insure_payinfo(self, message, title, amount, currency, target_addr, order_id, request_id):
        '''
        支付信息接口
        :param message:
        :param title:
        :param amount:
        :param currency:
        :param target_addr:
        :param order_id:
        :param request_id:
        :return:
        '''
        url = "https://sandboximb8.bixin.com/messenger/api/v3/transfer.c2bInfo"
        target_payment_url = "bixin://transfer/c2bDeposit"
        target_payment_date = { "message": message, "title": title, "amount": amount, "currency": currency, "target_addr": target_addr, "order_id": order_id, "request_id": request_id}

        query_string = urllib.parse.urlencode(target_payment_date)
        target_payment_uri = target_payment_url + '?' + query_string
        params = {"target_payment_uri": target_payment_uri}
        insure_pay = requests.get(url, headers=self.headers, params=params)
        return insure_pay

    def insure_pay(self, message, amount, payment_password, request_id, seq):
        '''
        :param message:
        :param amount:
        :param payment_password:
        :param request_id:request_id
        :param seq:
        :return:
        '''
        url = "https://sandboximb8.bixin.com/messenger/api/v3/transfer.create"
        payload_query = {
            'seq': seq,
            'amount': amount,
            'payment_password': payment_password,
            'message': message,
            'request_id': request_id
        }
        insure_pay = requests.post(url, headers=self.headers, data=payload_query)
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
              mapp_insure_create_order(deposit_order_id: "%s", puuid: "%s", unit: "%s", period: "%s" ) {
                ok
                err_msg
                err_code
                order_id
              }
            }''' % (deposit_order_id, puuid, unit, period)
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
        Mutation = '''{
        mapp_insure_order_list(
          status: "%s",
          page: %s,
          page_size: %s,
        ){
          total_pages
          order_list{
            uuid
            expire_at
            amount
            paid_amount
            paid_amount_currency
            insure_price_currency
            insure_period
            insure_price
            status
            insure_type
          }
        }
      }''' % (status, page, page_size)
        payload_query = {'query': Mutation}
        insure_list= requests.post(self.url_prefix, headers=self.headers, data=json.dumps(payload_query))
        return insure_list

    def insure_orderdetail(self, uuid):
        '''
        order详情页
        :param uuid:
        :return:
        '''
        Mutation = '''{
        mapp_insure_order_info(uuid: "%s"){
          confid_uuid
          uuid
          created_at
          updated_at
          expire_at
          expire_price
          insure_type
          amount
          amount_currency
          quote_amount
          insure_name
          current_price
          paid_amount
          paid_amount_currency
          expire_price_currency
          current_price_currency
          insure_amount_currency
          insure_price_currency
          insure_period
          insure_amount
          insure_price
          status
          paid_quote_amount
          paid_quote_amount_currency
        }
      }''' % uuid
        payload_query = {'query': Mutation}
        insure_detail = requests.post(self.url_prefix, headers=self.headers, data=json.dumps(payload_query))
        return insure_detail