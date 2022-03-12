# -*- coding: utf-8 -*-
# @Author : xiaowj
# @Time : 2022/3/2 22:55
import pymysql
from common.pubilc.request_getconfig import GetConfig


class DoSql:
    def do_sql(self,query):

        # 创建一个数据库链接,从配置文件拿到地址
        cnn = pymysql.connect(host=GetConfig.get_db_cofing("host"),
                              port=int(GetConfig.get_db_cofing("port")),
                              user=GetConfig.get_db_cofing("user"),
                              password=GetConfig.get_db_cofing("password"),
                              database=GetConfig.get_db_cofing("database"),
                              charset=GetConfig.get_db_cofing("charset"))

        # 游标cursor
        cursor = cnn.cursor()

        # 写sql语句
        query_sql = query

        #执行sql语句
        cursor.execute(query_sql)
        #获取结果 打印结果
        res = cursor.fetchone() #


        # 关闭游标
        cursor.close()

        # 关闭链接
        cnn.close()
        if res == None:
            return None
        else:
            return res[0]

if __name__ == '__main__':
    from common.pubilc.request_getdata import GetData
    report_id = DoSql().do_sql("SELECT reportId FROM yy_report as a LEFT JOIN yy_customer as b on a.customerId = b.customerId where b.`name` = '{}'  ORDER BY a.reportTime DESC LIMIT 1 ;".format(getattr(GetData,"customName")))
    pay_id = DoSql().do_sql("SELECT b.id from  yy_comm_project as a LEFT JOIN yy_pay_comm_plan as b on a.cycle_id = b.cycle_id where a.project_id = '{0}' and a.del = 0 and  '{1}' BETWEEN valid_start_time and valid_end_time ORDER BY b.id DESC LIMIT 1 ;".format(getattr(GetCookie,"projectId"),getattr(GetData,"projectId")))
    groupbuyPlanId = DoSql().do_sql("SELECT id FROM yy_comm_groupbuy_plan where cycle_id in (SELECT id FROM yy_comm_project_cycle where project_id = (SELECT id from yy_comm_project where project_id = {0})) and  '{1}' BETWEEN valid_start_time and valid_end_time and receivable_groupbuy != 0  LIMIT 1 ;".format(31,"2022-03-02"))

    print(groupbuyPlanId)

