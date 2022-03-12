# -*- coding: utf-8 -*-
# @Author : xiaowj
# @Time : 2022/2/26 16:59
import requests


class HttpRequest:
    def __init__(self,url,data,mode,headers):
        self.url = url
        self.data = data
        self.mode = mode
        self.headers = headers

    def http_request(self,cookies=None):
        if self.mode == "post":
            print("data 》》》",self.data)
            #print("headers 》》》", self.headers)
            res = requests.post(self.url,json=self.data,headers =self.headers,cookies=cookies)
            return res
        else:
            res = requests.get(self.url, headers =self.headers,json=self.data)
            return res

if __name__ == '__main__':
    url = "https://pre.yunjinji.cn/user-center/auth/staff/login"
    data = {"cityId": 306,
            "system": "android",
            "model": "phone",
            "appId": "commission",
            "uid": "",
            "areaCode": "+86",
            "account": "13100000008",
            "password": "123456"}
    headers = {"Connection":"Keep-Alive","Content-Type":"application/json;charset=utf-8"}
    r1 = HttpRequest(url,data,"post",headers).http_request()

    print(r1.json())
    print(r1.request.headers)