# -*- coding: utf-8 -*-
# @Author : xiaowj
# @Time : 2022/3/6 16:07
import re
from common.pubilc.request_getdata import GetData
class DoRegx:
    @staticmethod
    def do_regx(s):
        while re.search('\$\{(.*?)\}',s):
            key = re.search('\$\{(.*?)\}',s).group()
            value = re.search('\$\{(.*?)\}',s).group(1)
            s = s.replace(key,str(getattr(GetData,value)))
            print("key:",key)
            print("value:",value)

        return s

    @staticmethod
    def do_newstr_regx(s):
        while re.search('@(.*?)@',s):
            key = re.search('@(.*?)@',s).group()
            value = re.search('@(.*?)@',s).group(1)
            if str(getattr(GetData,value)) == "null":
                key = re.search('\"@(.*?)@\"',s).group()
                s=s.replace(key,str(getattr(GetData,value)))
            else:
                s = s.replace(key,str(getattr(GetData,value)))

        return s

    @staticmethod
    def do_repleacNone_regx(s):
        while re.search('None', s):
            s = s.replace('None','null')
        return s
if __name__ == '__main__':
    # str_s1 = '[{"cutAmount": 0.0, "divisionName": "测试部", "number": 1, "payedCut": 0.0, "ratio": 1.0, "userId": "055c509d3c1b4c2ebf2bc70fe8447e67", "userName": "驻场real"}, {"cutAmount": None, "divisionName": None, "number": 2, "payedCut": None, "ratio": None, "userId": None, "userName": None}, {"cutAmount": None, "divisionName": None, "number": 3, "payedCut": None, "ratio": None, "userId": None, "userName": None}]'
    # res = DoRegx().do_repleacNone_regx(str_s1)
    # print(res)

    str2 ='{"cityId":306,"platformId":${salePlatformId},"system":"android","model":"phone","appId":"commission","uid":"${zcjl_userid}","id":${tradeId}}'
    res = DoRegx().do_regx(str2)
    print(res)