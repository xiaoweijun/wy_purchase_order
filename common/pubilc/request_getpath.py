# -*- coding: utf-8 -*-
# @Author : xiaowj
# @Time : 2022/2/27 16:25
import os

project_path = os.path.split(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0])[0]

# 配置文件地址
config_path = os.path.join(project_path,"conf","httprequest.config")

# 测试报告地址
testreport_path = os.path.join(project_path,r"Result/test_report","rest_report.html")

# 普通认购单测试数据地址
testdata_path = os.path.join(project_path,"test_data","purchase.xlsx")




# 日志地址
logging_path = os.path.join(project_path,r"Result/test_logging","test_logging.txt")

print(config_path)
print(testreport_path)
print(testdata_path)