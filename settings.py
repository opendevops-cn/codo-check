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

### cmdb 读取get， 邮件发送post  用户信息get
api_user = 'publish'
api_pwd = 'shenshuo'

api_settings = dict(
    api_user=api_user,
    api_pwd=api_pwd,
    api_user_mfa='',
    api_gw=api_gw,
    mail_api=mail_api
)

"""
{
        "to_list": "shenshuo@shinezone.com",
        "subject": "这里是标题",
        "content": "这里是内容",
        "subtype": "plain"
}
"""
### 代码检查发送邮件  首先从api获取，如果获取不到,再配置获取
mail_to_dict = dict(
    do_cron="191715030@qq.com.com",
)
