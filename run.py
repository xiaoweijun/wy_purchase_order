# -*- coding: utf-8 -*-
# @Author : xiaowj
# @Time : 2022/2/26 20:03
import unittest,HTMLTestRunnerNew,smtplib

from common.pubilc import request_testcase
from common.pubilc import request_getpath
from common.pubilc.request_email import SendEmail
from common.pubilc.request_testcase import TestLogin


def run():

    suite = unittest.TestSuite()
    #suite.addTest(TestLogin("test_userlogin"))
    #方法二：TestLoader  创建一个加载器
    loader= unittest.TestLoader()


    #从测试名里去加载所有用例 TestMathMethod类
    #suite.addTest(loader.loadTestsFromTestCase(TestMathMethod))
    #执行整个文件里所有的测试用例
    suite.addTest(loader.loadTestsFromModule(request_testcase))

    with open(request_getpath.testreport_path, "wb") as file:
        runner = HTMLTestRunnerNew.HTMLTestRunner(stream=file,
                                                  verbosity=2,
                                                  title="wy测试报告（1）",
                                                  description="wyjjr第一次测试报告",
                                                  tester="肖炜君")
        runner.run(suite)
    #生成邮件后，发邮件
    SendEmail().send_email()
if __name__ == '__main__':
    run()