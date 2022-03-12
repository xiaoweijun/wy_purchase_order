# -*- coding: utf-8 -*-
# @Author : xiaowj
# @Time : 2022/3/6 5:14

import time
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.application import MIMEApplication
from common.pubilc import request_getpath
from common.pubilc.request_getconfig import GetConfig
# smtplib模块主要负责发送邮件：是一个发送邮件的动作，连接邮箱服务器，登录邮箱，发送邮件（有发件人，收信人，邮件内容）。
# email模块主要负责构造邮件：指的是邮箱页面显示的一些构造，如发件人，收件人，主题，正文，附件等。

now = time.strftime('%Y-%m-%d %H:%M:%S')
class SendEmail:
    def send_email(self):

        host_server = eval(GetConfig.get_email_to("host_server"))  #qq邮箱smtp服务器
        sender = eval(GetConfig.get_email_to("sender")) #发件人邮箱
        pwd = eval(GetConfig.get_email_to("pwd"))
        receiver = eval(GetConfig.get_email_to("email_to"))  # 收件人邮箱
        mail_title = 'wy认购单流程测试报告' #邮件标题
        mail_content = "您好，这是{0}生成的认购单的测试报告附件！".format(now) #邮件正文内容
        # 初始化一个邮件主体
        msg = MIMEMultipart()
        #主题
        msg["Subject"] = Header(mail_title,'utf-8')
        msg["From"] = sender
        msg['To'] = ";".join(receiver)
        # 邮件正文内容
        part = MIMEText(mail_content,'plain','utf-8')
        msg.attach(part)

        # 附件部分
        part = MIMEApplication(open(request_getpath.testreport_path,'rb').read())
        part.add_header("Content-Disposition","attachment",filename=request_getpath.testreport_path)
        msg.attach(part)
        smtp = SMTP_SSL(host_server) # ssl登录

        # login(user,password):
        # user:登录邮箱的用户名。
        # password：登录邮箱的密码，像笔者用的是网易邮箱，网易邮箱一般是网页版，需要用到客户端密码，需要在网页版的网易邮箱中设置授权码，该授权码即为客户端密码。
        smtp.login(sender,pwd)

        # sendmail(from_addr,to_addrs,msg,...):
        # from_addr:邮件发送者地址
        # to_addrs:邮件接收者地址。字符串列表['接收地址1','接收地址2','接收地址3',...]或'接收地址'
        # msg：发送消息：邮件内容。一般是msg.as_string():as_string()是将msg(MIMEText对象或者MIMEMultipart对象)变为str。
        smtp.sendmail(sender,receiver,msg.as_string())
        print("测试报告已发送至邮箱！")
        # quit():用于结束SMTP会话。
        smtp.quit()
if __name__ == '__main__':
    receiver = ['13729112152@163.com']  # 收件人邮箱
    SendEmail().send_email()