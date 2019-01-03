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


def get_conf(dbname, db_info):
    """获取SQL配置生产配置文件"""
    conf_file = '/tmp/' + uuid() + '.ini'
    print("conf_file  is " + conf_file)
    if len(str(base64.b64decode(db_info)).split(',,')) < 4:
        print('db_info error')
        exit(-100)

    db_host, db_port, db_user, db_pwd = str(base64.b64decode(db_info)).split(',,')
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


def exec_sqladvisor_v2(publish_name, db_info, db_name, sqls):
    print('exec db is {}'.format(publish_name))
    conf_file = get_conf(db_name, db_info)
    for s in sqls.split(';'):
        if s:
            sub2 = subprocess.Popen('sqladvisor -f {} -q "{};" -v 1'.format(conf_file, s), shell=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
            stdout, stderr = sub2.communicate()
            # ret = sub2.returncode
            print(stdout)


if __name__ == '__main__':
    fire.Fire(exec_sqladvisor_v2)
