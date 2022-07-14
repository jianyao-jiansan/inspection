# -*- coding:utf-8 -*-
# author: guomaoqiu
# desc: 将生成的图片以及日志内容发送至巡检展示平台

import requests
import base64
import json
import os
import time 


requests.DEFAULT_RETRIES = 5  # 增加重试连接次数
s = requests.session()
s.keep_alive = False  # 关闭多余连接


class SendToWeb():
  def __init__(self):
    # 巡检展示平台URL
    self.url = os.getenv('INSPECTION_WEB_API_URL')
    # 环境简称：
    self.env_simple_name = os.getenv("ENV_SIMPLE_NAME")
    # 环境中文名称：
    self.title = os.getenv('PLATFORM_ENV_NAME')
  
    """
    export INSPECTION_WEB_API_URL="http://9785-183-222-43-241.ngrok.io/receive"
    export ENV_SIMPLE_NAME=whcy
    export PLATFORM_ENV_NAME="武汉船用"
    """

  def get_log_data(self):
    content = ""
    inspection_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    text_list = ["【" + self.title.strip('"') + "根云平台环境日常巡检结果】" +"\n" + "巡检时间：{0}".format(inspection_time) + "\n"]

    # 这是基础信息服务的日志
    if os.path.exists("/tmp/patrol.log"):
        with open("/tmp/patrol.log", "r") as f:
            for i in f.readlines():
                text_list.append(i)
                content=("".join(text_list))
        f.close()
    else:
        print("patrol不存在")

    # 这是爬取网页的数据
    if os.path.exists("/tmp/inspection.log"):
        with open("/tmp/inspection.log", "r") as f:
            for i in f.readlines():
                text_list.append(i)
                content=("".join(text_list))
        f.close()
      
    return content

   


  def Go(self):
      if os.path.exists("/tmp/result.jpg") is True:
          #res = ""
          # 图片地址
          file_path='/tmp/result.jpg'
          # 图片名
          file_name=file_path.split('/')[-1]
          # 二进制打开图片
          file=open(file_path,'rb')
          # 拼接参数
          
          if os.path.exists("/tmp/system_info.json"):
              with open("/tmp/system_info.json", "r") as load_f:
                load_dict=json.load(load_f)
                simple_data = load_dict
                print(load_dict)

          with open(file_path, 'rb') as f :
              res = base64.b64encode(f.read())
              data={
              'filename': file_name,
              'base64code': res,
              'env_simple_name': self.env_simple_name,
              'content_data': self.get_log_data(),
              'env_name': os.getenv("PLATFORM_ENV_NAME"),
              'cpuinfo': simple_data["cpuinfo"], 
              'memoryinfo': simple_data["memoryinfo"],
              'diskused': simple_data["diskused"],
              'diskonhost': simple_data["diskonhost"],
              'diskmount': simple_data["diskmount"],
              'restartpods': simple_data["restartpods"],
              'unreadypods':  simple_data["unreadypods"],
              'unrunningpods': simple_data["unrunningpods"],
              'servertimestatus': simple_data["servertimestatus"]
              }
              print(data)    
          # 发送post请求到服务器端
          try:
            r = requests.post(url=self.url, data=(data), verify=False, timeout=10)
            print(r.status_code)
            print(r.content)
            # 获取服务器返回的图片，字节流返回
            if r.status_code == 200:
                print("发送至巡检展示平台成功")
          except Exception as e:
                print("发送至巡检展示平台失败", e)  
      else:
          print("/tmp/result.jpg 文件不存在....")

SendToWeb().Go()
exit()
