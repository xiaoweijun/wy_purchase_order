# -*- coding: utf-8 -*-
# @Author : xiaowj
# @Time : 2022/2/26 19:22
import configparser,os
from common.pubilc import request_getpath

class GetConfig:
    @staticmethod
    def get_config():
        #root_dir = os.path.dirname(os.path.abspath('.')) # 获取当前文件所在目录的上一级目录，即项目所在目录
        cf = configparser.ConfigParser()
        cf.read(request_getpath.config_path, encoding="utf-8")
        print("config配置文件的地址是：",request_getpath.config_path)

        return cf.get("MODE", "mode")

    #从配置文件中读取数据库地址
    @staticmethod
    def get_db_cofing(name):
        cf = configparser.ConfigParser()
        cf.read(request_getpath.config_path, encoding="utf-8")

        return cf.get("DB", name)

    @staticmethod
    def get_email_to(name):
        cf = configparser.ConfigParser()
        cf.read(request_getpath.config_path, encoding="utf-8")

        return cf.get("EMAIL", name)

if __name__ == '__main__':
    cf = GetConfig()
    print(cf.get_config())
    a = eval(cf.get_email_to("host_server"))
    print(a)
    print(type(a))