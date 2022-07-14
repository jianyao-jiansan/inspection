# -*- coding:utf8 -*-
# author: guomaoqiu
# desc: 执行入口脚本
import time
from retry_check import retry_check
# from disk_info import DiskUsage

if __name__ == "__main__":
    # DiskUsage().disk_calc()
    retry_check()
