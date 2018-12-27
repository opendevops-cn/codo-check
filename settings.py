#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Contact : 191715030@qq.com
Author  : shenshuo
Date    : 2018/8/9
Desc    : 
"""

api_gw = 'http://gw.shinezone.net.cn/api'
mail_api = '{}/mg/v2/notifications/mail/'.format(api_gw)
login_api = '{}/accounts/login/'.format(api_gw)
publish_info_api = '{}/task/v2/task_other/publish_cd/'.format(api_gw)
get_key_api = '{}/task/v2/task/accept/'.format(api_gw)

### cmdb 读取get， 邮件发送post  用户信息get
api_user = 'publish'
api_pwd = 'shenshuo'
api_key = 'JJFTQNLXHBYWSVSCINNEWNDFJRKWGY2UNJTTSVTLMN3UGUKXPFDE4NDH'

api_settings = dict(
    api_user=api_user,
    api_pwd=api_pwd,
    api_key=api_key,
    api_gw=api_gw,
    mail_api=mail_api,
    login_api=login_api,
    publish_info_api=publish_info_api,
    get_key_api=get_key_api,
)


sonar_domain = 'http://ops-sonar.shinezone.net.cn/dashboard/index/'
sonar_login = '0e8510011b3fb281d1737e13b7fdceadd6b601b4'
sonar_info =dict(
    sonar_login =sonar_login,
    sonar_domain = sonar_domain
)
### 代码检查发送邮件  首先从api获取，如果获取不到,再配置获取
mail_to_dict = {"shenshuo_server-test": "191715030@qq.com.com"}