#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Contact : 191715030@qq.com
Author  : shenshuo
Date    : 2018/8/9
Desc    : 执行代码扫描
"""

import fire
import os
import subprocess
from settings import sonar_info
from api_handler import API


def get_config_info(publish_name):
    obj = API()
    result = obj.get_publish_name_info(publish_name)
    return result[0]['repository'], result[0]['mail_to']


def exec_sonar_v2(publish_name, git_repository, publish_tag, mail_to):
    app_name = git_repository.split('/')[-1].replace(".git", "")
    print(app_name)
    ### 删除已经存在的，然后创建
    app_path = os.path.join('/var/www/version/', app_name)
    os.system('mkdir -p {}'.format(app_path))
    cmd1 = 'cd {} && rm -rf *'.format(app_path)
    os.system(cmd1)
    ## 代码获取完毕
    cmd = "cd {} && git clone -b {} {}".format(app_path, publish_tag, git_repository)
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
            "sonar.login={sonar_login}\n".format(key=app_name, name=publish_name,
                                                 sonar_login=sonar_info.get('sonar_login')))

    sub2 = subprocess.Popen("cd {}/{} && /usr/local/sonar-scanner/bin/sonar-scanner".format(app_path, app_name),
                            shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = sub2.communicate()

    for i in stdout.decode('utf-8').split('\n'):
        print(i)

    print("mail_to: ", mail_to)
    msg = "代码检查完毕！\n项目：{}\n应用：{}\n标签：{}\n用户名: shinezone \n密码：shinezone \n详情：{}{}".format(
        publish_name, app_name, publish_tag, sonar_info.get('sonar_domain'), app_name)
    obj = API()

    result = obj.send_mail_for_api(mail_to, '代码检查', msg)
    print(result)
    print("successful")


def main(publish_name, publish_tag):
    if publish_name == 'PUBLISH_NAME' or publish_tag == 'PUBLISH_TAG':
        print("[Error:] PUBLISH_NAME PUBLISH_TAG 不能为空")
        exit(-1)

    git_repository, mail_to = get_config_info(publish_name)
    if git_repository:
        exec_sonar_v2(publish_name, git_repository, publish_tag, mail_to)
    else:
        print('[Error:] git repository is none !!!')


if __name__ == '__main__':
    fire.Fire(main)
