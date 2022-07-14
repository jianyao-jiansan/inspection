#-*- coding:utf-8 -*-
# author: guomaoqiu
# desc: 工具箱

import os
import time
from os import listdir
import base64
import hashlib
from PIL import Image, ImageDraw, ImageFont

title = os.getenv("PLATFORM_ENV_NAME")


def get_file_base64(filepath):
    """ 获取文件base64 """
    try:
        if not os.path.isfile(filepath):
            return
        with open(filepath, "rb") as f:
            image = f.read()
            image_base64 = str(base64.b64encode(image), encoding='utf-8')
        print("    4.获取截图图片base64成功.")
        return image_base64
    except Exception as why:
        print("    4.获取截图图片base64失败.", why)

def get_file_md5(filepath):
    """ 获取文件md5 """
    try:
        if not os.path.isfile(filepath):
            return
        myhash = hashlib.md5()
        f = open(filepath, "rb")
        while True:
            b = f.read(8096)
            if not b:
                break
            myhash.update(b)
        f.close
        print("    5.获取截图图片MD5成功.\nkafka积压详情请看下图:")
        return myhash.hexdigest()
    except Exception as why:
        print("    5.获取截图图片MD5失败.")
 

def add_tag(img, file_name, title):
    """ 添加水印 """
    try:
        draw = ImageDraw.Draw(img)
        #  打码所需要的字体文件
        myfont = ImageFont.truetype('./fonts/STXINWEI.TTF', size=70)
        fillcolor = "#008000"
        width, height = img.size
        draw.text((width-1200, height-100), title + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),  fill=fillcolor, font=myfont)
        img.save("/tmp/" + file_name + ".jpg","jpeg")
        # img.show()
        print("      - 添加水印成功.")
    except Exception as why:
        print("      - 添加水印失败.", why)

def splice():
    """ 图片拼接 """
    try:
        # 这里处理一下排序
        files=os.listdir("/tmp/")
        files.sort()

        # 获取当前文件夹中所有JPG图像
        im_list = [Image.open("/tmp/" + fn) for fn in files if fn.endswith('.jpg')] 
        # 图片转化为相同的尺寸
        ims = []
        for i in im_list:
            new_img = i.resize((1480, 890), Image.BILINEAR)
            ims.append(new_img)
        # ims.sort()
        # 单幅图像尺寸
        width, height = ims[0].size
    
        # 创建空白长图
        result = Image.new(ims[0].mode, (width, height * len(ims)))
    
        # 拼接图片
        for i, im in enumerate(ims):
            result.paste(im, box=(0, i * height))
    
        # 保存图片
        result.save('/tmp/result.jpg')
        print("保存拼图成功")
 
    except Exception as e:
        print(e)


