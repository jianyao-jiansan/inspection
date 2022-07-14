# -*- coding:utf-8 -*-
# author: guomaoqiu
# desc: 根云平台登录，工况数据检查

import requests
import json
import datetime
import time
import os
import base64
import sys

# 自动化浏览器驱动
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui
from PIL import Image, ImageDraw, ImageFont

from tools import add_tag

class Inspection():
    def __init__(self):
        #########  env start #########
        self.env_domain = os.getenv("INSPECTION_DOMAIN")
        # 根云平台用户名
        self.username = os.getenv("INSPECTION_USERNAME")
        # 根英平台密码
        self.password = os.getenv("INSPECTION_PASSWORD")
        # 物实例URL
        self.thing_instace_url = os.getenv("INSPECTION_ROOTCLOUD_THING_INSTANCE_URL")
        # grafana时间段
        self.last_time = os.getenv("LAST_TIME")
        # 第二个监控项
        self.last_time2 = os.getenv("LAST_TIME2")

        # grafana kafka积压面板具体url
        self.grafana_kafka_lag_detail_url_n = os.getenv("GRAFANA_KAFKA_LAG_DETAIL_URL")
        self.grafana_kafka_lag_detail_url = self.grafana_kafka_lag_detail_url_n + self.last_time

        self.grafana_kafka_lag_detail_url_n2= os.getenv("GRAFANA_KAFKA_LAG_DETAIL_URL2")
        self.grafana_kafka_lag_detail_url2 = self.grafana_kafka_lag_detail_url_n2 + self.last_time2

        
        # gafana 登录url
        self.grafana_login_url = "http://grafana.{0}/login".format(self.env_domain)
        # grafana 用户名
        self.grafana_username = os.getenv("GRAFANA_USERNAME")
        # grafana 密码
        self.grafana_password = os.getenv("GRAFANA_PASSWORD")
        # 环境名称
        self.title = os.getenv("PLATFORM_ENV_NAME")

        # 引入打码功能
        self.add_tag = add_tag
        #########  env end #########

        ######## init chrome start ########
        chrome_options=Options()
        # 无头浏览器
        chrome_options.add_argument('--headless')
        # 取消沙盘模式
        chrome_options.add_argument('--no-sandbox') 
        # # 关闭浏览器提示信息
        # chrome_options.add_argument('disable-infobars') 
        # # 禁止默认浏览器检查
        # chrome_options.add_argument("no-default-browser-check")
        # chrome_options.add_argument("about:histograms")
        # chrome_options.add_argument("about:cache")
        # # 禁止扩展
        # chrome_options.add_argument("disable-extensions")

        self.browser = webdriver.Chrome(options=chrome_options)
        # 浏览器窗口大小设置
        self.browser.set_window_size(1480,980)
        ######## init chrome end ########


    def check_rootcloud(self):
        print("根云平台页面状态:")
        try:
            try:
                self.browser.get("http://console-ui.{0}/login".format(self.env_domain))
                # 发送账号
                print("    - 填充账户")
                self.browser.find_element(By.ID, "userId").send_keys(self.username)
                # 发送密码
                print("    - 填充密码")
                self.browser.find_element(By.ID, "password").send_keys(self.password)
                # 点击提交
                print("    - 提交登录")
                time.sleep(3)
                self.browser.find_element(By.XPATH, '//*[@id="__next"]/div/div/section/div/div/form/div[3]/div/div/span/button').click()
                # 等待加载
            except:
                self.browser.get("http://rootcloud-console.{0}/login".format(self.env_domain))
                # 发送账号
                print("    - 填充账户")
                self.browser.find_element(By.ID, "userId").send_keys(self.username)
                # 发送密码
                print("    - 填充密码")
                self.browser.find_element(By.ID, "password").send_keys(self.password)
                # 点击提交
                print("    - 提交登录")
                time.sleep(3)
                self.browser.find_element(By.XPATH, '//*[@id="__next"]/div/div/section/div/div/form/div[3]/div/div/span/button').click()
                # 等待加载

            time.sleep(15)
            # 判断登录之后查找主页面是否有 "接入与建模" 这个元素
            flag_text = (self.browser.find_element(By.XPATH, '//h1[text()="接入与建模"]').text)

            if (flag_text) ==  "接入与建模":
                print("    1.登录根云平台成功.")
                try:
                    self.browser.find_element(By.XPATH,"//button").click()
                    time.sleep(5)
                except:
                    pass
                # 进入 接入与建模页面
                # self.browser.find_element(By.XPATH, '//*[@id="__next"]/section/section/main/div/div[2]/div/div[1]').click()
                # 等待两秒进入后进入子页面
                # 注意当前 接入与建模页面是 iframe框架的子父页面
                # 如果直接去获取页面数据是没有办法拿到的，因为当前在父页面，所以这里直接访问子页面URL

                # 等待页面加载，获取进入子页面
                time.sleep(5)
                try:
                    self.browser.get("http://console-ui.{0}/service/cms".format(self.env_domain))
                    # 等待页面加载
                    time.sleep(10)
                    # 查找子页面中的关键字，以判断是否加载正常，这里查找的是在线设备数
                except:
                    self.browser.get("http://rootcloud-console.{0}/service/cms".format(self.env_domain))
                    # 等待页面加载
                    time.sleep(10)
                    # 查找子页面中的关键字，以判断是否加载正常，这里查找的是在线设备数
                keyboard=True    
                if keyboard:
                    # 等待3秒页面加载
                    time.sleep(10)

                    cms_device = "1_cms_device" + '.png'
                    path = os.path.join("/tmp/", cms_device)
        
                    try:
                        self.browser.get_screenshot_as_file(path)
                        print('    2.接入与建模页面加载成功，截图成功.')
                        image=Image.open(path)
                        image = image.convert("RGB")
                        self.add_tag(image, cms_device, self.title)
                    except Exception as e:
                        print('    2.接入与建模页面加载成功，截图失败',e)
                    
                    thing_instance = "2_thing_instance" + '.png'
                    path = os.path.join("/tmp/", thing_instance)

                    self.browser.get(self.thing_instace_url)
                    # 等待物实例列表加载
                    time.sleep(30)
                    # 寻找一个关键字作为判断物实例列表的加载情况

                    # 在线设备
                    #try:
                    #    self.browser.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/div/div[2]/div[4]/div/div[2]').click()
                    #except:
                    #    self.browser.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/div/div[2]/div/div[4]/div/div[2]').click()

                    #time.sleep(10)

                    # 点击 “在线”
                    #self.browser.find_element(By.XPATH,'/html/body/div[2]/div/div/div/div[2]/div/div/div/ul/li[1]').click()

                    #time.sleep(30)
                    instance_keyboard=True
                    if instance_keyboard:
                        try:
                            self.browser.get_screenshot_as_file(path)
                            print('    3.物实例页面加载成功，截图成功.')
                            image=Image.open(path)
                            image = image.convert("RGB")
                            self.add_tag(image, thing_instance, self.title)
                        except Exception as e:
                            print('    3.物实例页面加载成功，物实例页面截图失败',e)
                    else:
                        print("  物实例列表加载异常，请手动登录检查.")
                else:
                    print("    2.接入与建模页面加载异常, 请手动登录检查.")
            else:
                print("    1.登录根云平台失败.")
            time.sleep(2)
            # 退出浏览器
            self.browser.quit()
        except Exception as e:
            print(e)

    def grafana_kafka(self):
        print("Grafana监控面板状态:")
        try:
            self.browser.get(self.grafana_login_url)
            # time.sleep(2)
            # 这里是为了处理不同版本的grafana登录页面的元素位置不同
            try:
                print ("    - 填充账号")
                self.browser.find_element(By.XPATH, '//*[@id="login-view"]/form/div[1]/input').send_keys(self.grafana_username)
                print ("    - 填充密码")
                self.browser.find_element(By.XPATH, '//*[@id="login-view"]/form/div[2]/input').send_keys(self.grafana_password)
                print ("    - 提交登录")
                self.browser.find_element(By.XPATH, '//*[@id="login-view"]/form/div[3]/button').click()
            except:
                print ("    - 填充账号")
                self.browser.find_element(By.XPATH, '//*/form/div[1]/div[2]/div/div/input').send_keys(self.grafana_username)
                print ("    - 填充密码")
                self.browser.find_element(By.XPATH, '//*/form/div[2]/div[2]/div/div/input').send_keys(self.grafana_password)
                print ("    - 提交登录")
                self.browser.find_element(By.XPATH, '//*/div[2]/div/div/form/button').click()   
            time.sleep(5)

            # 判断cookies中是否有登录标识
            if "grafana_session" == self.browser.get_cookies()[0]['name']:
                print ("    1.登录Grafana成功")
                # time.sleep(3)
                self.browser.get(self.grafana_kafka_lag_detail_url)
                # 等待加载，这里如果加载时间不够，那么下面就会报错，导致中断
                time.sleep(10)
                # 点击max，从大到小排序
                self.browser.find_element(By.XPATH, "//table//*[text()='max']").click()

                # 保存文件
                file_name = "3_kafka" + '.png'
                path = os.path.join("/tmp/", file_name)

                
                try:
                    self.browser.get_screenshot_as_file(path)
                    print('    2.kafka积压监控面板截图成功.')
                    image=Image.open(path)
                    image = image.convert("RGB")
                    self.add_tag(image, file_name, self.title)
                  
                except Exception as why:
                    print('    2.kafka积压监控面板截图成功', why)
                # 关闭浏览器

                self.browser.get(self.grafana_kafka_lag_detail_url2)
                # 等待加载，这里如果加载时间不够，那么下面就会报错，导致中断
                time.sleep(40)
                # 点击max，从大到小排序
                self.browser.find_element(By.XPATH, "//table//*[text()='max']").click()

                                # 保存文件
                file_name = "4_kafka" + '.png'
                path = os.path.join("/tmp/", file_name)

                try:
                    self.browser.get_screenshot_as_file(path)
                    print('    3.kafka消费速率监控面板截图成功.')
                    image=Image.open(path)
                    image = image.convert("RGB")
                    self.add_tag(image, file_name, self.title)
                  
                except Exception as why:
                    print('    3.kafka消费速率监控面板截图成功', why)
                # 关闭浏览器
                self.browser.quit()
            else:
                print("   1.登录Grafana失败，请手动登录检查.")
        except Exception as e :
            print('    2.启动浏览器失败', e)
