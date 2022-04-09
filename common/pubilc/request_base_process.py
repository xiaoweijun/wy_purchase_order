# -*- coding: utf-8 -*-
# @Author : xiaowj
# @Time : 2022/4/7 18:05
from common.pubilc.request_getdata import GetData
class RequestProcess:
    def roleCutWayDtos_process(self,roleCutWayDtos_list):
        for item in roleCutWayDtos_list:
            # 拓展 提成方式
            if item["cutRoleId"] == 1:
                setattr(GetData,"expandCutCaseType",str(item["way"]))
                if item["fixedAmount"] == "null":
                    setattr(GetData, "expandFixedAmount","")
                else:
                    setattr(GetData,"expandFixedAmount",str(item["fixedAmount"]))
            # 拓展经理 提成方式
            elif item["cutRoleId"] == 2:
                setattr(GetData,"expandMgrCutCaseType",str(item["way"]))
                if item["fixedAmount"] == "null":
                    setattr(GetData, "expandMgrFixedAmount","")
                else:
                    setattr(GetData,"expandMgrFixedAmount",str(item["fixedAmount"]))
            # 驻场 提成方式
            elif item["cutRoleId"] == 3:
                setattr(GetData,"standCutCaseType",str(item["way"]))
                if item["fixedAmount"] == "null":
                    setattr(GetData, "fixedAmount","")
                else:
                    setattr(GetData,"fixedAmount",str(item["fixedAmount"]))
            # 驻场经理 提成方式
            elif item["cutRoleId"] == 4:
                setattr(GetData,"standManagerCutCaseType",str(item["way"]))
                if item["fixedAmount"] == "null":
                    setattr(GetData, "standManagerFixedAmount","")
                else:
                    setattr(GetData,"standManagerFixedAmount",str(item["fixedAmount"]))
            # 拓展总监 提成方式
            elif item["cutRoleId"] == 5:
                setattr(GetData,"expandDirectorCutCaseType",str(item["way"]))
                if item["fixedAmount"] == "null":
                    setattr(GetData, "expandDirectorFixedAmount","")
                else:
                    setattr(GetData,"expandDirectorFixedAmount",str(item["fixedAmount"]))
            # 区域总 提成方式
            elif item["cutRoleId"] == 6:
                setattr(GetData,"areaManagerCutCaseType",str(item["way"]))
                if item["fixedAmount"] == "null":
                    setattr(GetData, "areaManagerFixedAmount","")
                else:
                    setattr(GetData,"areaManagerFixedAmount",str(item["fixedAmount"]))


