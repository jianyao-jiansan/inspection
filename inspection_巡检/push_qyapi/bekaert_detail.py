# coding=utf-8

import requests
#import ssl
import time
#import json

'''
#跳过ssl
#context = ssl._create_unverified_context()

#获得token
token = requests.Session()

login_data = {"username":"ko+rp8n3Px+E0HrFTy0HmPLkGmykpHu3GMwo4JMkwRywQ0bo4mbTT6+5IeIhVcZtiYmgLCvXEHHaLp4Hy3iBjB1ngKEZplMWKOysDv4zpHmnm+\
4VG4jxjyPryxgX0c/ELJ32qI53zaQnwVbZF4WdLPlMniqKebUlacPNurgZ5u4=","password":"n7ETbSNt+Z8Qto73aO/rC3Dvp3cHzK2F+lZC1prjcFUOuaV1IQ9FBRsDz1TZC9\
up7Ce8rl6QYOBMpagS4DjtAoAAWLb1hkiGSnp1DleO1yZDN7ffTeFaP24tXkHjhEYRbNsxe5bZHaFEOIvUOazjtkYWRpSHlsvXcdQuXlpHUH0="}

# 
response = token.post('https://rootcloud-console.rciot.bekaert.com/api/auth/login', data = login_data, verify=False)
#print(response)
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------

#引用token访问
##DEVICE
ONLINE = token.get('https://rootcloud-console.rciot.bekaert.com/frame-cms/api/device/v2/thing/thing-instances?thingType=DEVICE&_\
includeMetadata=true&_limit=1&_skip=0&_sort=%5B%7B%22field%22%3A%20%22created%22%2C%20%22sortType%22%3A%20%22DESC%22%7D%5D&onlineType=ONLINE')
OFFLINE = token.get('https://rootcloud-console.rciot.bekaert.com/frame-cms/api/device/v2/thing/thing-instances?thingType=DEVICE&_\
includeMetadata=true&_limit=1&_skip=0&_sort=%5B%7B%22field%22%3A%20%22created%22%2C%20%22sortType%22%3A%20%22DESC%22%7D%5D&onlineType=OFFLINE')
NOT_ACTIVE = token.get('https://rootcloud-console.rciot.bekaert.com/frame-cms/api/device/v2/thing/thing-instances?thingType=DEVICE&_\
includeMetadata=true&_limit=1&_skip=0&_sort=%5B%7B%22field%22%3A%20%22created%22%2C%20%22sortType%22%3A%20%22DESC%22%7D%5D&onlineType=NOT_ACTIVE')
##复合物
COMPOSITE_THING = token.get('https://rootcloud-console.rciot.bekaert.com/frame-cms/api/device/v2/thing/thing-instances?thingType=COMPOSITE_THING&_\
includeMetadata=true&_limit=1&_skip=0&_sort=%5B%7B%22field%22%3A%20%22created%22%2C%20%22sortType%22%3A%20%22DESC%22%7D%5D')
##GATEWAY
ONLINE_GATEWAY = token.get('https://rootcloud-console.rciot.bekaert.com/frame-cms/api/device/v2/thing/thing-instances?thingType=GATEWAY&_includeMetadata=true&_\
limit=1&_skip=0&_sort=%5B%7B%22field%22%3A%20%22created%22%2C%20%22sortType%22%3A%20%22DESC%22%7D%5D&onlineType=ONLINE')
OFFLINE_GATEWAY = token.get('https://rootcloud-console.rciot.bekaert.com/frame-cms/api/device/v2/thing/thing-instances?thingType=GATEWAY&_includeMetadata=true&_limit=1&_\
skip=0&_sort=%5B%7B%22field%22%3A%20%22created%22%2C%20%22sortType%22%3A%20%22DESC%22%7D%5D&onlineType=OFFLINE')
NOT_ACTIVE_GATEWAY = token.get('https://rootcloud-console.rciot.bekaert.com/frame-cms/api/device/v2/thing/thing-instances?thingType=GATEWAY&_includeMetadata=true&_limit=1&_skip=0&_\
sort=%5B%7B%22field%22%3A%20%22created%22%2C%20%22sortType%22%3A%20%22DESC%22%7D%5D&onlineType=NOT_ACTIVE')
##物实例
OBJECT_INSTANCE = token.get('https://rootcloud-console.rciot.bekaert.com/frame-cms/api/device/devices/status/count?_groupBy=%5B%22state%22%5D')
##Xpaas
XPAAS_app_build = token.get('https://rootcloud-console.rciot.bekaert.com/frame-xpaas/app?&rc_in_wlpaass=true')
XPAAS_components = token.get('https://rootcloud-console.rciot.bekaert.com/frame-xpaas/compeco/market/componentsStore?&rc_in_wlpaass=true')
XPAAS_data = token.get('https://rootcloud-console.rciot.bekaert.com/frame-xpaas/project')

#print(OBJECT_INSTANCE.text)
#str截断
#NEW_OFFLINE = OFFLINE.text.split('null')
NEW_ONLINE = ONLINE.text.replace("null", "0").replace("true", "1").replace("false", "0")
NEW_OFFLINE = OFFLINE.text.replace("null", "0").replace("true", "1").replace("false", "0")
NEW_NOT_ACTIVE = NOT_ACTIVE.text.replace("null", "0").replace("true", "1").replace("false", "0")
NEW_COMPOSITE_THING = COMPOSITE_THING.text.replace("null", "0").replace("true", "1").replace("false", "0")
NEW_ONLINE_GATEWAY = ONLINE_GATEWAY.text.replace("null", "0").replace("true", "1").replace("false", "0")
NEW_OFFLINE_GATEWAY = OFFLINE_GATEWAY.text.replace("null", "0").replace("true", "1").replace("false", "0")
NEW_NOT_ACTIVE_GATEWAY = NOT_ACTIVE_GATEWAY.text.replace("null", "0").replace("true", "1").replace("false", "0")
NEW_OBJECT_INSTANCE = OBJECT_INSTANCE.text.replace("null", "0").replace("true", "1").replace("false", "0")
#print(NEW_OFFLINE)
#str转换为dict
ONLINE_dict = eval(NEW_ONLINE)
OFFLINE_dict = eval(NEW_OFFLINE)
NOT_ACTIVE_dict = eval(NEW_NOT_ACTIVE)
COMPOSITE_THING_dict = eval(NEW_COMPOSITE_THING)
ONLINE_GATEWAY_dict = eval(NEW_ONLINE_GATEWAY)
OFFLINE_GATEWAY_dict = eval(NEW_OFFLINE_GATEWAY)
NOT_ACTIVE_GATEWAY_dict = eval(NEW_NOT_ACTIVE_GATEWAY)
OBJECT_INSTANCE_dict = eval(NEW_OBJECT_INSTANCE)

"""
print("登录平台 %s" % response.status_code)
print("XPAAS_app_build %s" % XPAAS_app_build.status_code)
print("XPAAS_components %s" % XPAAS_components.status_code)
print("XPAAS_data %s" % XPAAS_data.status_code)
print("在线设备数 %s" % ONLINE_dict['metadata']['totalCount'])
print("离线设备数 %s" % OFFLINE_dict['metadata']['totalCount'])
print("未激活设备数 %s" % NOT_ACTIVE_dict['metadata']['totalCount'])
print("复合物数 %s" % COMPOSITE_THING_dict['metadata']['totalCount'])
print("网关在线设备数 %s" % ONLINE_GATEWAY_dict['metadata']['totalCount'])
print("网关离线设备数 %s" % OFFLINE_GATEWAY_dict['metadata']['totalCount'])
print("网关未激活设备数 %s" % NOT_ACTIVE_GATEWAY_dict['metadata']['totalCount'])
print("物实例数 %s" % OBJECT_INSTANCE_dict['payload'][0]['count'])
"""
'''
#tt = "登录平台 %s" % response.status_code

### A url列表
ONLINE = 'https://rootcloud-console.rciot.bekaert.com/frame-cms/api/device/v2/thing/thing-instances?thingType=DEVICE&_\
includeMetadata=true&_limit=1&_skip=0&_sort=%5B%7B%22field%22%3A%20%22created%22%2C%20%22sortType%22%3A%20%22DESC%22%7D%5D&onlineType=ONLINE'
OFFLINE = 'https://rootcloud-console.rciot.bekaert.com/frame-cms/api/device/v2/thing/thing-instances?thingType=DEVICE&_\
includeMetadata=true&_limit=1&_skip=0&_sort=%5B%7B%22field%22%3A%20%22created%22%2C%20%22sortType%22%3A%20%22DESC%22%7D%5D&onlineType=OFFLINE'
NOT_ACTIVE = 'https://rootcloud-console.rciot.bekaert.com/frame-cms/api/device/v2/thing/thing-instances?thingType=DEVICE&_\
includeMetadata=true&_limit=1&_skip=0&_sort=%5B%7B%22field%22%3A%20%22created%22%2C%20%22sortType%22%3A%20%22DESC%22%7D%5D&onlineType=NOT_ACTIVE'
##复合物
COMPOSITE_THING = 'https://rootcloud-console.rciot.bekaert.com/frame-cms/api/device/v2/thing/thing-instances?thingType=COMPOSITE_THING&_\
includeMetadata=true&_limit=1&_skip=0&_sort=%5B%7B%22field%22%3A%20%22created%22%2C%20%22sortType%22%3A%20%22DESC%22%7D%5D'
##GATEWAY
ONLINE_GATEWAY = 'https://rootcloud-console.rciot.bekaert.com/frame-cms/api/device/v2/thing/thing-instances?thingType=GATEWAY&_includeMetadata=true&_\
limit=1&_skip=0&_sort=%5B%7B%22field%22%3A%20%22created%22%2C%20%22sortType%22%3A%20%22DESC%22%7D%5D&onlineType=ONLINE'
OFFLINE_GATEWAY = 'https://rootcloud-console.rciot.bekaert.com/frame-cms/api/device/v2/thing/thing-instances?thingType=GATEWAY&_includeMetadata=true&_limit=1&_\
skip=0&_sort=%5B%7B%22field%22%3A%20%22created%22%2C%20%22sortType%22%3A%20%22DESC%22%7D%5D&onlineType=OFFLINE'
NOT_ACTIVE_GATEWAY = 'https://rootcloud-console.rciot.bekaert.com/frame-cms/api/device/v2/thing/thing-instances?thingType=GATEWAY&_includeMetadata=true&_limit=1&_skip=0&_\
sort=%5B%7B%22field%22%3A%20%22created%22%2C%20%22sortType%22%3A%20%22DESC%22%7D%5D&onlineType=NOT_ACTIVE'
##物实例
OBJECT_INSTANCE = 'https://rootcloud-console.rciot.bekaert.com/frame-cms/api/device/devices/status/count?_groupBy=%5B%22state%22%5D'
##Xpaas
XPAAS_app_build = 'https://rootcloud-console.rciot.bekaert.com/frame-xpaas/app?&rc_in_wlpaass=true'
XPAAS_components = 'https://rootcloud-console.rciot.bekaert.com/frame-xpaas/compeco/market/componentsStore?&rc_in_wlpaass=true'
XPAAS_data = 'https://rootcloud-console.rciot.bekaert.com/frame-xpaas/project'

A = [ONLINE, OFFLINE, NOT_ACTIVE, COMPOSITE_THING, ONLINE_GATEWAY, OFFLINE_GATEWAY, NOT_ACTIVE_GATEWAY]
B = [XPAAS_app_build, XPAAS_components, XPAAS_data]
C = OBJECT_INSTANCE
# 监测URL是否正常响应
def url_check(url):
    # 当前时间
    check_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print("开始监测：%s -- %s" % (url, check_time))
    try:
        # 请求URL, 设置3s超时
        #r = requests.get(url, timeout=3)
        login_potal = 'https://rootcloud-console.rciot.bekaert.com/api/auth/login'
        login_data = {"username":"ko+rp8n3Px+E0HrFTy0HmPLkGmykpHu3GMwo4JMkwRywQ0bo4mbTT6+5IeIhVcZtiYmgLCvXEHHaLp4Hy3iBjB1ngKEZplMWKOysDv4zpHmnm+\
                     4VG4jxjyPryxgX0c/ELJ32qI53zaQnwVbZF4WdLPlMniqKebUlacPNurgZ5u4=","password":"n7ETbSNt+Z8Qto73aO/rC3Dvp3cHzK2F+lZC1prjcFUOuaV1IQ9FBRsDz1TZC9\
                     up7Ce8rl6QYOBMpagS4DjtAoAAWLb1hkiGSnp1DleO1yZDN7ffTeFaP24tXkHjhEYRbNsxe5bZHaFEOIvUOazjtkYWRpSHlsvXcdQuXlpHUH0="}
        ##保存token
        token = requests.Session()
        response = token.post(login_potal, data = login_data, verify=False, timeout=3)
        #引用token
        r = token.get(url, timeout=3)
        if r.status_code != 200:
            # 请求响应状态异常
            msg = "监控的URL: %s%sHttp状态异常: %s%s监测时间: %s" % (url, "\n\n", r.status_code, "\n\n", check_time)
            print("监测结果：异常(Http状态异常:%s) -- %s" % (r.status_code, check_time))
            # 通过云推推送消息
            yuntui_push(msg)
        else:
            # 请求响应正常
            NEW_ONLINE_ALL = r.text.replace("null", "0").replace("true", "1").replace("false", "0")
            DEVICE_dict_all = eval(NEW_ONLINE_ALL)
            msg = "监控的URL: %s%s %s%sHttp状态正常: %s%s监测时间: %s" % (url, "\n\n", DEVICE_dict_all['metadata']['totalCount'], "\n\n", r.status_code, "\n\n", check_time)
            #msg = "监控的URL: %s%s %s" % (url, "\n\n", DEVICE_dict_all['metadata']['totalCount'])
            print("监测结果：正常 -- %s" % check_time)
            yuntui_push(msg)
    except requests.exceptions.ConnectTimeout:
        # 请求响应超时
        msg = "监控的URL: %s%s请求异常: %s%s监测时间: %s" % (url, "\n\n", "请求超时", "\n\n", check_time)
        print("监测结果：超时 -- %s" % check_time)
        # 通过云推推送消息
        yuntui_push(msg)

# 将预警消息通过云推推送
def yuntui_push(content):
    # 当前时间
    push_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # 云推接口的信息配置，可以通过 https://tui.juhe.cn 自行注册创建
    # (可以配置邮件、钉钉机器人、微信公众号等接收方式)

    webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=a425cf34-eaab-4fcf-a523-0b6cff7edce4"
    headers = {"Content-Type":"application/json"}
    data = {
          "msgtype": "text",
          "text": {
              "content": content,
              "mentioned_list":[]
          }
      }
    try:
        r = requests.post(url=webhook_url,headers=headers, json=data, verify=False)
        #r = requests.post("https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=a425cf34-eaab-4fcf-a523-0b6cff7edce4", data=data, verify=False, timeout=15)
        push_res = r.status_code
#        print(push_res)
#        push_res = json.loads(r.content)
#        print(push_res)
#        print(push_res['code'])
#        code = push_res['code']
        code = push_res
        if code == 200:
            print("推送结果：成功 -- %s" % push_time)
        else:
            print("推送结果：失败(%s) -- %s" % (push_res['reason'], push_time))
    except requests.exceptions.ConnectTimeout:
        print("推送结果：超时 -- %s" % push_time)

# 执行URL可用性监测
if __name__ == '__main__':
    # 监控URL可用性
    for i in range(0, len(A)):
        url_check(A[i])
#        print(A[i])
#    url_check(XPAAS_data)
    