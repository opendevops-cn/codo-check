#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Contact : 191715030@qq.com
Author  : shenshuo
Date    : 2018/8/9
Desc    : 执行代码扫描
修改BUG：没有检测过的项目 先创建对应的目录  2018年8月16日     沈硕
修改BUG：修复邮件不能发送多人的BUG        2018年8月16日     沈硕
"""

import fire
import os
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

mail_dict = dict()

mail_addr = {}

try:
    from settings import *
except:
    pass


class ITResEmail:
    def __init__(self, subject, message, email_to):
        self.subject = subject
        self.message = message
        self.smtp_name = mail_addr['smtp_name']
        self.smtp_port = mail_addr['smtp_port']
        self.email_name = mail_addr['email_name']
        self.email_pwd = mail_addr['email_pwd']
        self.email_cc = mail_addr['email_cc']
        self.email_to = email_to

    def init_email(self):
        self.to_email(self.email_to, self.email_cc)

    def to_email(self, email_to, email_cc):
        msg = MIMEText(self.message, 'plain', 'utf-8')
        msg['Subject'] = self.subject
        msg['From'] = formataddr([self.email_name, self.email_name])
        msg['To'] = email_to

        if email_to == '':
            server = smtplib.SMTP(self.smtp_name, self.smtp_port)
            server.login(self.email_name, self.email_pwd)
            server.sendmail(self.email_name, [email_cc], msg.as_string())
        else:
            msg['Cc'] = formataddr([email_cc, email_cc])
            server = smtplib.SMTP(self.smtp_name, self.smtp_port)
            server.login(self.email_name, self.email_pwd)
            server.sendmail(self.email_name, [email_to, email_cc], msg.as_string())
        server.quit()


def exec_sonar(git_url, short_name, tag):
    ### 仓库地址   运维简称   标签
    if short_name == "APP_NAME" or git_url == "GIT_URL":
        print("APP_NAME GIT_URL 不能为空")
        exit(-1)

    print("git url: " + git_url)
    print("git tag: " + tag)
    app_name = git_url.split('/')[1].replace(".git", "")

    ### 删除已经存在的，然后创建
    app_path = os.path.join('/var/www/version/', short_name)
    os.system('mkdir -p {}'.format(app_path))
    cmd1 = 'cd {} && rm -rf *'.format(app_path)
    os.system(cmd1)
    ## 代码获取完毕
    cmd = "cd {} && git clone -b {} {}".format(app_path, tag, git_url)
    print(cmd)
    sub1 = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = sub1.communicate()
    ret = sub1.returncode
    if ret != 0:
        print(stdout, stderr)
        exit(-2)

    ## 写入扫描文件
    print("start checking code")
    sonar_file = os.path.join(app_path, app_name, "sonar-project.properties")
    with open(sonar_file, 'w') as f:
        f.write(
            "sonar.projectKey={key}\n"
            "sonar.projectName={name}\n"
            "sonar.projectVersion=1.0\n"
            "sonar.sources=.\n"
            "sonar.login=0e8510011b3fb281d1737e13b7fdceadd6b601b4\n".format(key=app_name, name=short_name))

    sub2 = subprocess.Popen("cd {}/{} && /usr/local/sonar-scanner/bin/sonar-scanner".format(app_path, app_name),
                            shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = sub2.communicate()

    mail_to = mail_dict.get(short_name, 'shenshuo@shinezone.com')
    print("mail_to: ", mail_to)
    msg = "代码检查完毕！\n项目：{}\n应用：{}\n标签：{}\n用户名: shinezone \n密码：shinezone \n详情：http://ops-sonar.shinezone.net.cn/dashboard/index/{}".format(
        short_name, app_name, tag, app_name)
    m = ITResEmail("代码检查", msg, mail_to)
    m.init_email()
    for i in stdout.decode('utf-8').split('\n'):
        print(i)

    print("successful")


if __name__ == '__main__':
    fire.Fire(exec_sonar)
