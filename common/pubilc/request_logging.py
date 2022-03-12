# -*- coding: utf-8 -*-
# @Author : xiaowj
# @Time : 2022/2/28 20:53
from common.pubilc.request_getpath import logging_path
import logging

class RequestLogging:

    def my_logging(self,msg,level):
        # 定义一个日志收集器 my_logger
        my_logger = logging.getLogger("wy_logging")
        # 设置级别
        my_logger.setLevel("DEBUG")

        # 设置输出格式
        formatter = logging.Formatter('%(asctime)s-%(levelname)s-%(filename)s-%(name)s-日志信息:%(message)s')

        # 创建一个输出渠道
        ch = logging.StreamHandler()
        ch.setLevel("DEBUG")
        ch.setFormatter(formatter)

        fh = logging.FileHandler(logging_path, encoding="utf-8")
        fh.setLevel("DEBUG")
        fh.setFormatter(formatter)

        # 两者对接--指定输出渠道
        my_logger.addHandler(ch)
        my_logger.addHandler(fh)

        # 收集日志
        if level == "DEBUG":
            my_logger.debug(msg)
        elif level == "INFO":
            my_logger.info(msg)
        elif level == "WARNING":
            my_logger.warning(msg)
        elif level == "ERROR":
            my_logger.error(msg)
        elif level == "CRITICAL":
            my_logger.critical(msg)
        # 关闭渠道
        my_logger.removeHandler(ch)
        my_logger.removeHandler(fh)


    def debug_log(self,msg):
        self.my_logging(msg,"DEBUG")

    def info_log(self,msg):
        self.my_logging(msg,"INFO")

    def warning_log(self,msg):
        self.my_logging(msg,"WARNING")

    def error_log(self,msg):
        self.my_logging(msg,"ERROR")

    def critical_log(self,msg):
        self.my_logging(msg,"CRITICAL")


