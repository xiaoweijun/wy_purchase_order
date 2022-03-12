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

        return s

if __name__ == '__main__':
    str_s1 = '{"cityId": 306,"system":${tradeId} "android","model": "phone","appId": "commission","uid": "","areaCode": "+86","account": "${jszz_tel}","password": "123456"${cw_tel}“}'
    res = DoRegx().do_regx(str_s1)
    print(res)