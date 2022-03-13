# -*- coding: utf-8 -*-
# @Author : xiaowj
# @Time : 2022/2/26 19:50
import unittest,json
from common.pubilc.request_test import HttpRequest
from common.pubilc.request_do_excel import GetTestData
from common.pubilc.request_getconfig import GetConfig
from common.pubilc.request_getdata import GetData
from common.pubilc.request_logging import RequestLogging
from common.pubilc.request_do_sql import DoSql
from ddt import ddt,data

my_logger = RequestLogging()




# 登录测试用例数据
user_data = GetTestData().get_login_user()
# 认购单测试用例数据
purchase_mode = GetConfig.get_purchase_mode_config()
purchase_order_data = GetTestData().get_data(purchase_mode)
# 收佣测试用例数据
rec_mode = GetConfig.get_rec_mode_config()
rec_data =  GetTestData().get_data(rec_mode)
# 结佣测试用例数据
pay_mode = GetConfig.get_pay_mode_config()
pay_data = GetTestData().get_data(pay_mode)



# 1、用户登录 2、认购单 3、收佣单 4、结佣单
@ddt
class TestLogin(unittest.TestCase):
    # 用户登录获取到userid 和 cookie
    @data(*user_data)
    def test_1userlogin(self,user_data):
        res = HttpRequest(getattr(GetData,"login_url"), user_data["data"], user_data["method"],
                          eval(user_data["headers"])).http_request(None)
        TestResult = ""
        try:
            if "role_code" in user_data.keys():
                print("cookie的值是：{0},类型是{1}".format(res.cookies.get("satoken"),type(res.cookies.get("satoken"))))
                GetTestData().wirte_userid("user", res.json()["data"]["loginId"],res.cookies.get("satoken"), user_data["role_code"])
                setattr(GetData,user_data["role_cookie"],res.cookies)

            else:
                pass
            self.assertEqual(user_data["assert_info"], res.json()["msg"], msg="出问题了")
            TestResult = "Pass"
        except AssertionError as e:
            my_logger.info_log("{0}登录失败:{1}".format(user_data["role_code"],e))
            TestResult = "Failed"
            raise e

        finally:
            my_logger.info_log("获取到的结果是：{0}".format(res.json()))
        # 普通 or 代理认购单流程

    @data(*purchase_order_data)
    def test_2purchase_order(self, test_data):

        # 替换report_id
        if test_data["data"].find("@reportID@") != -1:
            test_data["data"] = test_data["data"].replace("@reportID@", str(getattr(GetData, "reportID")))
        # 替换认购单id
        if test_data["data"].find("@tradeId@") != -1:
            test_data["data"] = test_data["data"].replace("@tradeId@", str(getattr(GetData, "tradeId")))

        print("data 》》》", json.loads(test_data["data"]))
        print("cookie的值是：{0},类型是{1}".format(getattr(GetData, test_data["role_cookie"]),
                                            type(getattr(GetData, test_data["role_cookie"]))))
        my_logger.info_log(str(getattr(GetData, test_data["role_cookie"])))
        res = HttpRequest(test_data["url"], json.loads(test_data["data"]), test_data["method"],
                          eval(test_data["headers"])).http_request(getattr(GetData, test_data["role_cookie"]))

        # 生成报备单后，取到报备单id
        if test_data["url"].find("pretrade/report/add") != -1:
            setattr(GetData, "reportID", DoSql().do_sql(
                "SELECT reportId FROM yy_report as a LEFT JOIN yy_customer as b on a.customerId = b.customerId where b.`name` = '{0}'  ORDER BY a.reportTime DESC LIMIT 1 ;".format(
                    getattr(GetData, "customName"))))
            room_num = int(getattr(GetData, "roomNo_num"))
            GetTestData().updata_roomno("report_data", room_num + 1)
        # 生成认购单后，取到认购单id
        elif test_data["url"].find("purchase/first/submit") != -1:
            setattr(GetData, "tradeId", DoSql().do_sql(
                "SELECT id FROM yy_purchase_order where report_id = '{0}' and platform_id = '{1}' ORDER BY id desc LIMIT 1;".format(
                    getattr(GetData, "reportID"), getattr(GetData, "salePlatformId"))))

        print("获取到得cookies》》》", res.cookies.get("satoken"))
        # 写进测试结果，成功写入pass，失败写入failed
        TestResult = ""
        # 断言

        try:
            self.assertEqual(test_data["assert_info"], res.json()["msg"], msg="出问题了")
            TestResult = "Pass"
        except AssertionError as e:
            my_logger.info_log("用例执行失败:{0}".format(e))
            # print("用例执行失败:{0}".format(e))
            TestResult = "Failed"
            raise e
        finally:
            # 写进测试结果，成功写入pass，失败写入failed
            GetTestData().wirte_data(test_data["sheet_name"], int(test_data["case_id"]), str(res.json()), TestResult)
            my_logger.info_log("获取到的结果是：{0}".format(res.json()))

    # 普通收佣单流程
    @data(*rec_data)
    def test_3rec_comm_ticket(self, rec_data):
        # receivable_commision
        setattr(GetData, "receivable_commision", DoSql().do_sql(
            "SELECT receivable_commision from yy_purchase_order where id = {0};".format(
                str(getattr(GetData, "tradeId")))))
        if rec_data["data"].find("@tradeId@") != -1:
            rec_data["data"] = rec_data["data"].replace("@tradeId@", str(getattr(GetData, "tradeId")))

        if rec_data["data"].find("@rec_ticketId@") != -1:
            rec_data["data"] = rec_data["data"].replace("@rec_ticketId@", str(getattr(GetData, "rec_ticketId")))

        if rec_data["data"].find("@receivable_commision@") != -1:
            rec_data["data"] = rec_data["data"].replace("@receivable_commision@",
                                                        str(getattr(GetData, "receivable_commision")))

        res = HttpRequest(rec_data["url"], json.loads(rec_data["data"]), rec_data["method"],
                          eval(rec_data["headers"])).http_request(getattr(GetData, rec_data["role_cookie"]))
        TestResult = ""
        # 断言
        if rec_data["url"].find("commission/ticket/manual/create") != -1:
            setattr(GetData, "rec_ticketId", DoSql().do_sql(
                "SELECT ticket_id from yy_rec_comm_ticket_order where order_id = '{0}'".format(
                    getattr(GetData, "tradeId"))))
        try:
            self.assertEqual(rec_data["assert_info"], res.json()["msg"], msg="出问题了")
            TestResult = "Pass"
        except AssertionError as e:
            my_logger.info_log("用例执行失败:{0}".format(e))
            # print("用例执行失败:{0}".format(e))
            TestResult = "Failed"
            raise e
        finally:
            # 写进测试结果，成功写入pass，失败写入failed
            GetTestData().wirte_data(rec_data["sheet_name"], int(rec_data["case_id"]), str(res.json()), TestResult)
            my_logger.info_log("获取到的结果是：{0}".format(res.json()))

    # 结佣单流程
    @data(*pay_data)
    def test_4pay_comm_ticket(self, pay_data):
        setattr(GetData, "payable_commission", DoSql().do_sql(
            "SELECT payable_commission from yy_purchase_order where id = {0};".format(
                str(getattr(GetData, "tradeId")))))
        setattr(GetData, "receivable_commision", DoSql().do_sql(
            "SELECT receivable_commision from yy_purchase_order where id = {0};".format(
                str(getattr(GetData, "tradeId")))))
        if pay_data["data"].find("@tradeId@") != -1:
            pay_data["data"] = pay_data["data"].replace("@tradeId@", str(getattr(GetData, "tradeId")))

        if pay_data["data"].find("@pay_ticketId@") != -1:
            pay_data["data"] = pay_data["data"].replace("@pay_ticketId@", str(getattr(GetData, "pay_ticketId")))

        if pay_data["data"].find("@payable_commission@") != -1:
            pay_data["data"] = pay_data["data"].replace("@payable_commission@",
                                                        str(getattr(GetData, "payable_commission")))

        if pay_data["data"].find("@receivable_commision@") != -1:
            pay_data["data"] = pay_data["data"].replace("@receivable_commision@",
                                                        str(getattr(GetData, "receivable_commision")))

        res = HttpRequest(pay_data["url"], json.loads(pay_data["data"]), pay_data["method"],
                          eval(pay_data["headers"])).http_request(getattr(GetData, pay_data["role_cookie"]))
        TestResult = ""
        if pay_data["url"].find("/manual/create") != -1:
            setattr(GetData, "pay_ticketId", DoSql().do_sql(
                "SELECT ticket_id from yy_pay_comm_ticket_order where order_id = '{0}'".format(
                    getattr(GetData, "tradeId"))))
        try:
            self.assertEqual(pay_data["assert_info"], res.json()["msg"], msg="出问题了")
            TestResult = "Pass"
        except AssertionError as e:
            my_logger.info_log("用例执行失败:{0}".format(e))
            # print("用例执行失败:{0}".format(e))
            TestResult = "Failed"
            raise e
        finally:
            # 写进测试结果，成功写入pass，失败写入failed
            GetTestData().wirte_data(pay_data["sheet_name"], int(pay_data["case_id"]), str(res.json()), TestResult)
            my_logger.info_log("获取到的结果是：{0}".format(res.json()))



if __name__ == '__main__':
    unittest.main()
