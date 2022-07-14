# coding=utf-8

import requests
import ssl
import time
import json

#跳过ssl
context = ssl._create_unverified_context()

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