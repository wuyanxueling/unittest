# to run this test: python -m testtools.run bixin_test.py
# -*- coding: utf-8 -*-
from testtools import TestCase
import requests
import json
from time import sleep, time


class BixinClient(object)

    def __init__(self, cookies_file, token):
        self.session = requests.Session()
        self.headers = {
            'Cookie': cookies_file,
            'Content-Type': 'application/json',
            'User-Agent': UA,
            'X-Access-Token': token
        }
        self.url_prefix = "https://sandboximb9.bixin.com"

    def request_get(self, api, url_params=None):
        '''
        定义get请求方法
        :param api: 接口api
        :param url_params: URL含参数/URL不含参数
        :return: 返回请求
        '''
        if url_params:
            url = self.url_prefix + api + '?' + url_params
            result = self.session.get(url, headers=self.headers)
        else:
            url = self.url_prefix + api
            result = self.session.get(url, headers=self.headers)
        return result

    def request_post(self, api, payload):
        '''
        定义post请求方法
        :param api: 接口api
        :param payload: post接口请求
        :return: 返回请求值
        '''
        url = self.url_prefix + api
        result = self.session.post(url, headers=self.headers, data=json.dumps(payload))
        return result

    def profile_me(self):
        '''
        我的-修改资料
        :return: 资料信息
        '''
        api = '/messenger/api/v2/profile.me'
        profile_result = self.request_get(api)
        return profile_result

class BixinTestCase(TestCase):

    def setUp(self):
        super(BixinTestCase, self).setUp()
        cookies_file_A = "djlanguage=zh-hans; browser=0-yVojGb9o1iWyUYFfgeAw; bixin_session_id=m8gtd2hxcc0j0g3zu58iizsce8dd9ylq"  # cookies 文件路径
        token_A = "74f048b9bcff4c68ae569929a61dcde2"  # CRFS token
        cookies_file_B = ""  # cookies 文件路径
        token_B = ""  # CRFS token
        self.client_A = BixinClient(cookies_file_A, token_A)
        self.client_B = BixinClient(cookies_file_B, token_B)

    def test_profile(self):
        res = self.client_A.profile_me()
        self.assertEqual(200, res.status_code)  # 判断 用户B 资产接口

