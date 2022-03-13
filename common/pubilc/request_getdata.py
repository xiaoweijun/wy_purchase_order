# -*- coding: utf-8 -*-
# @Author : xiaowj
# @Time : 2022/2/26 22:35
from openpyxl import load_workbook
from common.pubilc import request_getpath
from common.pubilc.request_do_sql import DoSql
class GetData:

    reportID = "@reportID@"  #报备单id
    tradeId = "@tradeId@"   #认购单id
    #radeId = "2956"
    login_url = "https://pre.yunjinji.cn/user-center/auth/staff/login"  #登录的url

    #从excel中获取账号
    zc_tel= load_workbook(request_getpath.testdata_path)["user"].cell(2,1).value #驻场
    zcjl_tel= load_workbook(request_getpath.testdata_path)["user"].cell(3,1).value #驻场经理
    cw_tel = load_workbook(request_getpath.testdata_path)["user"].cell(4, 1).value #财务
    jszy_tel = load_workbook(request_getpath.testdata_path)["user"].cell(5, 1).value #结算专员
    tz_tel = load_workbook(request_getpath.testdata_path)["user"].cell(6, 1).value #拓展
    jszz_tel = load_workbook(request_getpath.testdata_path)["user"].cell(7, 1).value #结算组长
    qyz_tel = load_workbook(request_getpath.testdata_path)["user"].cell(8, 1).value #区域总
    zjb_tel = load_workbook(request_getpath.testdata_path)["user"].cell(9, 1).value #总经办
    xftz_tel = load_workbook(request_getpath.testdata_path)["user"].cell(10, 1).value #销方拓展

    # 从excel获取userid
    zc_userid = load_workbook(request_getpath.testdata_path)["user"].cell(2,3).value
    zcjl_userid = load_workbook(request_getpath.testdata_path)["user"].cell(3, 3).value
    cw_userid = load_workbook(request_getpath.testdata_path)["user"].cell(4, 3).value
    jszy_userid = load_workbook(request_getpath.testdata_path)["user"].cell(5, 3).value
    tz_userid = load_workbook(request_getpath.testdata_path)["user"].cell(6, 3).value
    jszz_userid = load_workbook(request_getpath.testdata_path)["user"].cell(7, 3).value
    qyz_userid = load_workbook(request_getpath.testdata_path)["user"].cell(8, 3).value
    zjb_userid = load_workbook(request_getpath.testdata_path)["user"].cell(9, 3).value
    xftz_userid = load_workbook(request_getpath.testdata_path)["user"].cell(10, 3).value

    # 用户cookie
    zc_cookie = None
    zcjl_cookie = None
    cw_cookie = None
    jszy_cookie = None
    tz_cookie = None
    jszz_cookie = None
    qyz_cookie = None
    zjb_cookie = None
    xftz_cookie = None

    salePlatformId = load_workbook(request_getpath.testdata_path)["report_data"].cell(3, 3).value #平台id
    projectId= load_workbook(request_getpath.testdata_path)["report_data"].cell(4, 3).value #楼盘id
    reportTime = load_workbook(request_getpath.testdata_path)["report_data"].cell(5, 3).value #报备时间
    visitTime = load_workbook(request_getpath.testdata_path)["report_data"].cell(6, 3).value  #到访时间
    purchaseDate = load_workbook(request_getpath.testdata_path)["report_data"].cell(7, 3).value  #认购时间
    roomNo_num = load_workbook(request_getpath.testdata_path)["report_data"].cell(1, 4).value
    roomNo = load_workbook(request_getpath.testdata_path)["report_data"].cell(1, 3).value + str(roomNo_num)   #房号
    customName = load_workbook(request_getpath.testdata_path)["report_data"].cell(2, 3).value + str(roomNo_num)  # 客户姓名
    agent_salePlatformId = load_workbook(request_getpath.testdata_path)["report_data"].cell(8, 3).value #代理成交平台id





    #从数据库获取reporid
    #reportID = DoSql().do_sql("SELECT reportId FROM yy_report as a LEFT JOIN yy_customer as b on a.customerId = b.customerId where b.`name` = '{0}'  ORDER BY a.reportTime DESC LIMIT 1 ;".format(str(customName)))

    # 结佣方案id
    pay_id = DoSql().do_sql("SELECT b.id from  yy_comm_project as a LEFT JOIN yy_pay_comm_plan as b on a.cycle_id = b.cycle_id where a.project_id = '{0}' and a.del = 0 and  '{1}' BETWEEN valid_start_time and valid_end_time ORDER BY b.id DESC LIMIT 1 ;".format(projectId,purchaseDate))
    #团购方案
    groupbuyPlanId = DoSql().do_sql("SELECT id FROM yy_comm_groupbuy_plan where cycle_id in (SELECT id FROM yy_comm_project_cycle where project_id = (SELECT id from yy_comm_project where project_id = {0})) and  '{1}' BETWEEN valid_start_time and valid_end_time and receivable_groupbuy != 0  LIMIT 1 ;".format(projectId,purchaseDate))

    #收佣方案id
    rec_id = DoSql().do_sql("SELECT b.id from  yy_comm_project as a LEFT JOIN yy_rec_comm_plan as b on a.cycle_id = b.cycle_id where a.project_id = '{0}' and a.del = 0 and  '{1}' BETWEEN valid_start_time and valid_end_time ORDER BY b.id DESC LIMIT 1;".format(projectId,purchaseDate))

    # 平台公司id collectingCompanyId
    collectingCompanyId = DoSql().do_sql("SELECT company_id from yy_comm_project_cycle where project_id = (SELECT id FROM yy_comm_project where project_id = {0}) LIMIT 1;".format(projectId))

    # rec_ticketId 收佣单id
    rec_ticketId = "@rec_ticketId@"
    # pay_ticket 结佣单id
    pay_ticketId = "@pay_ticketId@"
    #认购单的应收佣金
    receivable_commision = "@receivable_commision@"
    # 认购单的应结佣金
    payable_commission = "@payable_commission@"
    #公司账户id、名称
    account_id = DoSql().do_sql("SELECT id FROM yy_comm_self_account where platform_id = '{0}' LIMIT 1;".format(salePlatformId))
    account_name = DoSql().do_sql("SELECT account_name FROM yy_comm_self_account where platform_id = '{0}' LIMIT 1;".format(salePlatformId))

if __name__ == '__main__':
    setattr(GetData,"Cookie","123456")   #设置属性值
    print("判断是否有这个属性：",hasattr(GetData, "Cookie"))   #判断是否有这个属性
    print(getattr(GetData,"Cookie"))  #获取属性值
    delattr(GetData,"Test_attribute")  # 删除这个属性
    print("判断是否有这个属性：", hasattr(GetData, "Test_attribute"))
    print(getattr(GetData,"zc_tel1"))

