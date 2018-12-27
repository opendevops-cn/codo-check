#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Contact : 191715030@qq.com
Author  : shenshuo
Date    : 2018/12/25
Desc    : 
"""

import pyotp
import requests
import json
from settings import api_settings



class API(object):
    def __init__(self):
        self.url = api_settings['api_gw']
        self.user = api_settings['api_user']
        self.pwd = api_settings['api_pwd']
        self.key = api_settings.get('api_key')
        self.login_api = api_settings.get('login_api')
        self.publish_info_api = api_settings.get('publish_info_api')
        self.get_key_api = api_settings.get('get_key_api')
        self.mail_api = api_settings.get('mail_api')

    @property
    def get_mfa(self):
        t = pyotp.TOTP(self.key)
        return t.now()

    def login(self):
        try:
            headers = {"Content-Type": "application/json"}
            params = {"username": self.user, "password": self.pwd, "dynamic": self.get_mfa}
            result = requests.post(self.login_api, data=json.dumps(params), headers=headers)

            ret = json.loads(result.text)
            if ret['code'] == 0:
                return ret['auth_key']
            else:
                print(ret)
                print(ret['msg'])
                exit(1)
        except Exception as e:
            print('[Error:] 用户:{} 接口登陆失败，错误信息：{}'.format(self.user, e))

    def get_publish_name_info(self, publish_name):
        token = self.login()
        try:
            params = {'key': 'publish_name', 'value': publish_name}
            res = requests.get(self.publish_info_api, params=params, cookies=dict(auth_key=token))
            ret = json.loads(res.content)
            if ret['code'] == 0: return ret['data']
        except Exception as e:
            print('[Error:] Publish发布接口连接失败，错误信息：{}'.format(e))
            exit(-2)

    def get_publish_all_info(self):
        '''获取发布配置所有信息'''
        try:
            token = self.login()
        except Exception as e:
            print(e)
            token = self.login()

        res = requests.get(self.publish_info_api, cookies=dict(auth_key=token))
        ret = json.loads(res.content)
        if ret['code'] == 0: return ret['data']

    def send_mail_for_api(self, mail_list, mail_subject, mail_content):
        """发送邮件"""
        try:
            token = self.login()
        except Exception as e:
            print(e)
            token = self.login()

        req1 = requests.get(self.get_key_api, cookies=dict(auth_key=token))
        if req1.status_code != 200:
            raise SystemExit(req1.status_code)

        ret1 = json.loads(req1.text)
        if ret1['code'] == 0:
            csrf_key = ret1['csrf_key']
        else:
            raise SystemExit(ret1['code'])

        body = json.dumps({"to_list": mail_list, "subject": mail_subject, "content": mail_content, "subtype": "plain"})
        res = requests.post(self.mail_api, data=body, cookies=dict(auth_key=token, csrf_key=csrf_key))
        if res.status_code != 200:
            raise SystemExit(res.status_code)
        else:
            return json.loads(res.text)['msg']
