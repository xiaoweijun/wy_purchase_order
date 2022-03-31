# -*- coding: utf-8 -*-
# @Author : xiaowj
# @Time : 2022/2/26 19:50
import unittest,json,pytest
from common.pubilc.request_test import HttpRequest
from common.pubilc.request_do_excel import GetTestData
from common.pubilc.request_getconfig import GetConfig
from common.pubilc.request_getdata import GetData
from common.pubilc.request_logging import RequestLogging
from common.pubilc.request_do_sql import DoSql
from common.pubilc.request_do_regx import DoRegx
from common.pubilc import request_getpath
from ddt import ddt,data
# 日志实例
my_logger = RequestLogging()

# 登录测试用例数据
user_data = GetTestData(request_getpath.report_and_user_path).get_login_user()
# 认购单测试用例数据
purchase_mode = GetConfig.get_purchase_mode_config()
purchase_order_data = GetTestData().get_data(purchase_mode)
# 收佣测试用例数据
rec_mode = GetConfig.get_rec_mode_config()
rec_data =  GetTestData().get_data(rec_mode)
# 结佣测试用例数据
pay_mode = GetConfig.get_pay_mode_config()
pay_data = GetTestData().get_data(pay_mode)

checkout_mode=GetConfig.get_checkout_mode_config()
checkout_data = GetTestData().get_data(checkout_mode)

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
                #GetTestData().wirte_userid("user", res.json()["data"]["loginId"],res.cookies.get("satoken"), user_data["role_code"])
                setattr(GetData,user_data["role_code"]+"_userid",res.json()["data"]["loginId"])
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

        test_data["data"] = DoRegx.do_newstr_regx(test_data["data"])

        if test_data["url"].find("trade/first/approve") != -1:
            test_data["data"] = DoRegx.do_repleacNone_regx(test_data["data"])

        elif test_data["url"].find("trade/finalCheck/approve") != -1:
            test_data["data"] = DoRegx.do_repleacNone_regx(test_data["data"])
        print("data 》》》{0}", test_data["data"])
        print("cookie的值是：{0},类型是{1}".format(getattr(GetData, test_data["role_cookie"]),
                                            type(getattr(GetData, test_data["role_cookie"]))))
        my_logger.info_log(str(getattr(GetData, test_data["role_cookie"])))
        res = HttpRequest(test_data["url"], json.loads(test_data["data"]), test_data["method"],
                          eval(test_data["headers"])).http_request(getattr(GetData, test_data["role_cookie"]))
        print("url >>>{0}".format(type(test_data["url"])))
        # 生成报备单后，取到报备单id
        if test_data["url"].find("pretrade/report/add") != -1:
            setattr(GetData, "reportID", DoSql().do_sql(
                "SELECT reportId FROM yy_report as a LEFT JOIN yy_customer as b on a.customerId = b.customerId where b.`name` = '{0}'  ORDER BY a.reportTime DESC LIMIT 1 ;".format(
                    getattr(GetData, "customName"))))
            room_num = int(getattr(GetData, "roomNo_num"))
            GetTestData(request_getpath.report_and_user_path).updata_roomno("report_data", room_num + 1)
        # 生成认购单后，取到认购单id
        elif test_data["url"].find("purchase/first/submit") != -1:
            setattr(GetData, "tradeId", DoSql().do_sql(
                "SELECT id FROM yy_purchase_order where report_id = '{0}' and platform_id = '{1}' ORDER BY id desc LIMIT 1;".format(
                    getattr(GetData, "reportID"), getattr(GetData, "salePlatformId"))))

        elif test_data["url"].find("order/cut/detail/get") != -1 and test_data["case_id"] == 3 :
            setattr(GetData,"zc_cut",str(res.json()["data"]["currentStandCut"]["standRatioDtos"]).replace("\'", "\""))
            print("获取到的zc_cut >>>{0}".format(res.json()["data"]["currentStandCut"]["standRatioDtos"]))

        elif test_data["url"].find("order/cut/detail/get") != -1 and test_data["case_id"] == 8 :
            expandManagers = res.json()["data"]["currentExpandManager"]["expandManagers"]
            expandRatios_json = res.json()["data"]["currentExpandCut"]["expandRatios"]
            setattr(GetData,"areaManager",res.json()["data"]["currentStandManager"]["areaManager"])
            setattr(GetData,"areaManagerId",res.json()["data"]["currentStandManager"]["areaManagerId"])
            setattr(GetData,"standManager",res.json()["data"]["currentStandManager"]["standManager"])
            setattr(GetData,"standManagerId",res.json()["data"]["currentStandManager"]["standManagerId"])
            setattr(GetData,"standManagerRatio",res.json()["data"]["currentStandManager"]["standManagerRatio"])
            for i in range(3):
                del expandRatios_json[i]["cutAmount"]
                del expandRatios_json[i]["payedCut"]
                if i == 0:
                    setattr(GetData,"ex1_userId",str(expandRatios_json[i]["userId"]).replace("None", "null"))
                    setattr(GetData,"ex1_userName",str(expandRatios_json[i]["userName"]).replace("None", "null"))
                    setattr(GetData,"ex1_ratio",str(expandManagers[i]["ratio"]).replace("None", "null"))
                    setattr(GetData,"ex1_superiorId",str(expandManagers[i]["superiorId"]).replace("None", "null"))
                    setattr(GetData,"ex1_superiorName",str(expandManagers[i]["superiorName"]).replace("None", "null"))
                    setattr(GetData,"ex1_superiorSuperiorId",str(expandManagers[i]["superiorSuperiorId"]).replace("None", "null"))
                    setattr(GetData,"ex1_superiorSuperiorName",str(expandManagers[i]["superiorSuperiorName"]).replace("None", "null"))

                if i == 1:
                    setattr(GetData, "ex2_userId", str(expandRatios_json[i]["userId"]).replace("None", "null"))
                    setattr(GetData, "ex2_userName", str(expandRatios_json[i]["userName"]).replace("None", "null"))
                    setattr(GetData, "ex2_ratio", str(expandManagers[i]["ratio"]).replace("None", "null"))
                    setattr(GetData, "ex2_superiorId", str(expandManagers[i]["superiorId"]).replace("None", "null"))
                    setattr(GetData, "ex2_superiorName", str(expandManagers[i]["superiorName"]).replace("None", "null"))
                    setattr(GetData, "ex2_superiorSuperiorId",str(expandManagers[i]["superiorSuperiorId"]).replace("None", "null"))
                    setattr(GetData, "ex2_superiorSuperiorName",str(expandManagers[i]["superiorSuperiorName"]).replace("None", "null"))
                if i == 2:
                    setattr(GetData, "ex3_userId", str(expandRatios_json[i]["userId"]).replace("None", "null"))
                    setattr(GetData, "ex3_userName", str(expandRatios_json[i]["userName"]).replace("None", "null"))
                    setattr(GetData, "ex3_ratio", str(expandManagers[i]["ratio"]).replace("None", "null"))
                    setattr(GetData, "ex3_superiorId", str(expandManagers[i]["superiorId"]).replace("None", "null"))
                    setattr(GetData, "ex3_superiorName", str(expandManagers[i]["superiorName"]).replace("None", "null"))
                    setattr(GetData, "ex3_superiorSuperiorId",str(expandManagers[i]["superiorSuperiorId"]).replace("None", "null"))
                    setattr(GetData, "ex3_superiorSuperiorName",str(expandManagers[i]["superiorSuperiorName"]).replace("None", "null"))
                    setattr(GetData, "expandRatios", str(expandRatios_json).replace("None", "null").replace("\'", "\""))
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
            my_logger.info_log("获取到的结果是：{0}".format(res.text))

    # 收佣单流程
    @data(*rec_data)
    def test_3rec_comm_ticket(self, rec_data):
        # receivable_commision
        setattr(GetData, "receivable_commision", DoSql().do_sql(
            "SELECT receivable_commision from yy_purchase_order where id = {0};".format(
                str(getattr(GetData, "tradeId")))))
        rec_data["data"] = DoRegx.do_newstr_regx(rec_data["data"])

        res = HttpRequest(rec_data["url"], json.loads(rec_data["data"]), rec_data["method"],
                          eval(rec_data["headers"])).http_request(getattr(GetData, rec_data["role_cookie"]))
        print("url >>>{0}".format(rec_data["url"]))
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
        pay_data["data"] = DoRegx.do_newstr_regx(pay_data["data"])
        # if pay_data["data"].find("@tradeId@") != -1:
        #     pay_data["data"] = pay_data["data"].replace("@tradeId@", str(getattr(GetData, "tradeId")))


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

    # 退房流程
    @data(*checkout_data)
    def test_5check_out(self,checkout_data):
        checkout_data["data"] = DoRegx.do_newstr_regx(checkout_data["data"])
        res = HttpRequest(checkout_data["url"], json.loads(checkout_data["data"]), checkout_data["method"],
                          eval(checkout_data["headers"])).http_request(getattr(GetData, checkout_data["role_cookie"]))
        TestResult = ""

        try:
            self.assertEqual(checkout_data["assert_info"], res.json()["msg"], msg="出问题了")
            TestResult = "Pass"

        except AssertionError as e:
            my_logger.info_log("用例执行失败:{0}".format(e))
            # print("用例执行失败:{0}".format(e))
            TestResult = "Failed"
            raise e

        finally:
            # 写进测试结果，成功写入pass，失败写入failed
            GetTestData().wirte_data(checkout_data["sheet_name"], int(checkout_data["case_id"]), str(res.json()), TestResult)
            my_logger.info_log("获取到的结果是：{0}".format(res.json()))


if __name__ == '__main__':
    unittest.main()
    #pytest.main()

