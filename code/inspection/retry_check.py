# -*- coding:utf-8 -*- 
# author: guomaoqiu
# desc: 在完成第一遍运行之后测运行结果，直到最大重试次数
import os 
import time
from inspection import Inspection

def img_nums():
    """ 统计文件数字 """
    img_num = 0
    image_list = [
            "/tmp/1_cms_device.png",
            "/tmp/2_thing_instance.png",
            "/tmp/3_kafka.png",
            "/tmp/4_kafka.png"
        ]
    for img in image_list:
        if (os.path.isfile(img)):
            img_num +=1
    return img_num 

def retry_check():
    if img_nums() != 4:
        retry_count = 0
        while retry_count < 5:
            print("【第 {0} 次】".format(retry_count + 1))
            Inspection().check_rootcloud()
            time.sleep(2)
            Inspection().grafana_kafka()
            if img_nums() == 4:
                exit()
            retry_count += 1
            if retry_count == 5:
                exit()
