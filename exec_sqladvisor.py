#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
author : shenshuo
date   : 2018年4月24日
desc   : 执行SQL优化
1. 更新生成配置   data: 2018年6月1日
"""

import fire
import base64
import subprocess
from shortuuid import uuid
from api_handler import API


def get_conf(dbname, db_info):
    """获取SQL配置生产配置文件"""
    conf_file = '/tmp/' + uuid() + '.ini'
    print("conf_file  is " + conf_file)
    if len(str(base64.b64decode(db_info)).split(',,,')) < 4:
        print('db_info error')
        exit(-100)

    db_host, db_port, db_user, db_pwd = str(base64.b64decode(db_info), 'utf-8').split(',,,')
    print(db_host, db_port, db_user)
    if db_pwd == 'null':
        db_pwd = ''
    with open(conf_file, 'w') as f:
        f.write("[sqladvisor]\n"
                "username={db_user}\n"
                "password={db_pwd}\n"
                "host={db_host}\n"
                "port={db_port}\n"
                "dbname={dbname}\n"
                .format(db_user=db_user, db_pwd=db_pwd, db_host=db_host, db_port=db_port, dbname=dbname))
    return conf_file


def exec_sqladvisor_v2(db_name, conf_file, sqls, mail_to):
    print('exec db is {}'.format(db_name))

    for s in sqls.split(';'):
        if s:
            sub2 = subprocess.Popen('sqladvisor -f {} -q "{};" -v 1'.format(conf_file, s), shell=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
            stdout, stderr = sub2.communicate()
            result = stdout.decode('utf-8').replace('\n\n', '\n')
            print(result)
            ### 发送邮件
            msg = "SQL优化完毕！\n库名：{}\n语句：{}\n详情：{}".format(db_name, sqls, result)
            obj = API()

            res = obj.send_mail_for_api(mail_to, 'SQL索引优化', msg)
            print(res)


def main(publish_name, db_name, sqls):
    if publish_name == 'PUBLISH_NAME' or db_name == 'DB_NAME':
        print("[Error:] PUBLISH_NAME DB_NAME 不能为空")
        exit(-1)

    obj = API()
    result = obj.get_publish_name_info(publish_name)
    publish_hosts_api, mail_to = result[0]['publish_hosts_api'], result[0]['mail_to']

    print(publish_hosts_api, mail_to)
    if publish_hosts_api:
        res = obj.get_api_info(publish_hosts_api)
        for db in res['db_list']:
            if db['db_type'] == 'MySQL' and db['db_role'] == 'master':

                db_info = db['db_info']
                conf_file = get_conf(db_name, db_info)
                exec_sqladvisor_v2(db_name, conf_file, sqls, mail_to)
        print("successful")
    else:
        print('[Error:] git repository is none !!!')


if __name__ == '__main__':
    fire.Fire(main)
