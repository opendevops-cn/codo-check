#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
author : shenshuo
date   : 2018年4月24日
role   ：执行SQL优化
python3 pymysql 连接Inception ，在判断版本时会出现value error 问题
修改 pymysql connections.py
def _request_authentication(self):
    # https://dev.mysql.com/doc/internals/en/connection-phase-packets.html#packet-Protocol::HandshakeResponse
    if self.server_version.split('.', 1)[0] == 'Inception2':
        self.client_flag |= CLIENT.MULTI_RESULTS
    elif int(self.server_version.split('.', 1)[0]) >= 5:
        self.client_flag |= CLIENT.MULTI_RESULTS
"""

import fire
import base64
import subprocess
import warnings
import socket
import re

warnings.filterwarnings('ignore')
import pymysql

### 必填 可以从api获取
git_domain = ''
git_ssh = "git@{}".format(git_domain)

def _is_ip(value):
    """检测是否是IP"""
    ipv4_re = re.compile(r'^(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}$')
    if ipv4_re.match(value): return True


def conver_url2ip(db_host):
    '''RDS URL 解析成IP,不然host过长,导致inception无法备份'''
    if not _is_ip(db_host):
        old_host = db_host
        db_host = socket.gethostbyname(db_host)
        print('[HOST URL] %s ===> [IP]%s' % (old_host, db_host))
    return db_host


def get_conf(db_info):
    """获取SQL配置生产配置文件"""
    db_mark, db_host, db_port, db_user, db_pwd = str(base64.b64decode(db_info), "utf-8").split(',,')
    db_host = conver_url2ip(db_host)
    if db_pwd == 'null':
        db_pwd = ''
    connstr_target = dict(host=db_host, port=db_port, user=db_user, password=db_pwd, charset='utf8mb4')
    connstr_inception = {'host': '127.0.0.1', 'port': 6669, 'user': '', 'password': '', 'db': '',
                         'charset': 'utf8mb4'}

    return connstr_target, connstr_inception


def get_sql(db_file):
    gitlab = db_file.split(str(git_domain))
    if len(gitlab) != 2:
        return -1, '请输入正确的文件名'

    git_group = gitlab[1].split('blob')[0].split('/')
    git_branch = gitlab[1].split('blob')[1].split('/')[1]
    git_url = '{}:{}/{}.git'.format(git_ssh, git_group[1], git_group[2])
    ###
    cmd1 = 'mkdir -p /tmp/codes/ && cd /tmp/codes/ && rm -rf {} && git clone {} && cd {} && git checkout {}'.format(
        git_group[2], git_url, git_group[2], git_branch)
    sql_file = '/tmp/codes/{}/{}'.format(git_group[2], gitlab[1].split('blob')[1].replace('/' + git_branch + '/', ''))
    sub1 = subprocess.Popen(cmd1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = sub1.communicate()
    ret = sub1.returncode
    if ret == 0:
        with open(sql_file, "r") as f1:
            return 0, f1.read()
    else:
        return -1, stderr


def exec_inception(mark, db_info, db_file):
    print(mark)
    ### 获取要执行的SQL
    exec_code, exec_sql = get_sql(db_file)
    if exec_code != 0:
        print(exec_sql)
        exit(-1)

    # 执行还是校验
    operation = '--execute=1'
    # operation = '--enable-execute;--enable-ignore-warnings;--enable-force'

    # 发布目标服务器
    connstr_target, connstr_inception = get_conf(db_info)

    try:
        # 将待执行的sql语句组合成inception识别的格式
        sql_with_format = '''/*--user={};--password={};--host={};{};--port={};*/ inception_magic_start;\n{}\ninception_magic_commit;'''.format(
            connstr_target['user'],
            connstr_target['password'],
            connstr_target['host'],
            operation,
            connstr_target['port'], exec_sql)

        print(exec_sql)

        # 连接至inception 服务器
        conn_inception = pymysql.connect(host=connstr_inception.get('host', '127.0.0.1'),
                                         port=connstr_inception.get('port', 6669),
                                         user=connstr_inception.get('user', ''),
                                         password=connstr_inception.get('password', ''),
                                         charset=connstr_inception.get('charset', 'utf8mb4'))

        cur = conn_inception.cursor()

        cur.execute(sql_with_format)
        result = cur.fetchall()
        num_fields = len(cur.description)
        field_names = [i[0] for i in cur.description]
        print(field_names)
        # 打印出来Inception对MySQL语句的审计结果
        result_code = []
        for row in result:
            print(row[0], "|", row[1], "|", row[2], "|", row[3], "|", row[4], "|", row[5], "|", row[6], "|", row[7],
                  "|", row[8], "|", row[9], "|", row[10])
            result_code.append(row[2])

        cur.close()
        conn_inception.close()

        if 2 or 1 in result_code:
            print('There is a serious error, please check the log !!!')
            exit(-1)

    except  Exception as err:
        print(err)
        exit(-2)
    finally:
        print('****************')
        exit(-3)


if __name__ == '__main__':
    fire.Fire(exec_inception)
