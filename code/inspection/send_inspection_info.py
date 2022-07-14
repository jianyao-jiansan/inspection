#-*- coding:utf-8 -*-
# author: guomaoqiu
# desc: 获取巡检信息通知脚本

import sys
import json
import os
import requests
import time
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from tools import get_file_base64, get_file_md5, splice

# 企微机器人URL
webhook_url = os.getenv("QIWEI_URL")

# 昭才个人群
webhook_url2 = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=c5bc3ed6-1db8-441e-bd01-faeefe93241f"

title = os.getenv("PLATFORM_ENV_NAME")

# 是否需要发送
# 0：是
# 1：否
issend = os.getenv("ISSEND")

def send_msg():

    content = ""

    inspection_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    text_list = ["【" + title.strip('"') + "根云平台环境日常巡检结果】" +"\n" + "巡检时间：{0}".format(inspection_time) + "\n"]

    # 这是基础信息服务的日志
    if os.path.exists("/tmp/patrol.log"):
        with open("/tmp/patrol.log", "r") as f:
            for i in f.readlines():
                text_list.append(i)
                content=("".join(text_list))
        f.close()
    else:
        print("partol不存在")

    # 这是爬取网页的数据
    if os.path.exists("/tmp/patrol.log"):
        with open("/tmp/inspection.log", "r") as f:
            for i in f.readlines():
                text_list.append(i)
                content=("".join(text_list))
        f.close()

    headers = {"Content-Type":"application/json"}
    data = {
          "msgtype": "text",
          "text": {
              "content": content,
              "mentioned_list":[]
          }
      }
    r = requests.post(url=webhook_url,headers=headers, json=data, verify=False)  
    r2 = requests.post(url=webhook_url2,headers=headers, json=data, verify=False)  
    print(r.status_code)
    print(r2.status_code)

def send_img():
    """ 发送图片 """
    splice()
    headers = {"Content-Type":"application/json"}
    data = {
      "msgtype": "image",
      "image": {
              "base64": get_file_base64("/tmp/result.jpg"),
              "md5": get_file_md5("/tmp/result.jpg")
          }
      }
    r = requests.post(url=webhook_url,headers=headers, json=data, verify=False)
    r2 = requests.post(url=webhook_url2,headers=headers, json=data, verify=False)  
    print(r.status_code)
    print(r2.status_code)

if __name__ == "__main__":
    if issend == "0":
        # 发送文本
        send_msg()
        # 发送图片
        send_img()
    else:
        print("*** 此环境无外网访问权限，此消息无需发送. ***")

