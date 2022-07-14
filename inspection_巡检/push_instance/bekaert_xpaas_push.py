# coding=utf-8
import requests
from prometheus_client import CollectorRegistry,Gauge,push_to_gateway

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

url_dict = {"https://rootcloud-console.rciot.bekaert.com/frame-cms/api/device/v2/thing/thing-instances?thingType=DEVICE&_\
includeMetadata=true&_limit=1&_skip=0&_sort=%5B%7B%22field%22%3A%20%22created%22%2C%20%22sortType%22%3A%20%22DESC%22%7D%5D&onlineType=ONLINE":"ONLINE",
 "https://rootcloud-console.rciot.bekaert.com/frame-cms/api/device/v2/thing/thing-instances?thingType=DEVICE&_\
includeMetadata=true&_limit=1&_skip=0&_sort=%5B%7B%22field%22%3A%20%22created%22%2C%20%22sortType%22%3A%20%22DESC%22%7D%5D&onlineType=OFFLINE":"OFFLINE",
 "https://rootcloud-console.rciot.bekaert.com/frame-cms/api/device/v2/thing/thing-instances?thingType=DEVICE&_\
includeMetadata=true&_limit=1&_skip=0&_sort=%5B%7B%22field%22%3A%20%22created%22%2C%20%22sortType%22%3A%20%22DESC%22%7D%5D&onlineType=NOT_ACTIVE":"NOT_ACTIVE",
 "https://rootcloud-console.rciot.bekaert.com/frame-cms/api/device/v2/thing/thing-instances?thingType=COMPOSITE_THING&_\
includeMetadata=true&_limit=1&_skip=0&_sort=%5B%7B%22field%22%3A%20%22created%22%2C%20%22sortType%22%3A%20%22DESC%22%7D%5D":"COMPOSITE_THING",
 "https://rootcloud-console.rciot.bekaert.com/frame-cms/api/device/v2/thing/thing-instances?thingType=GATEWAY&_includeMetadata=true&_\
limit=1&_skip=0&_sort=%5B%7B%22field%22%3A%20%22created%22%2C%20%22sortType%22%3A%20%22DESC%22%7D%5D&onlineType=ONLINE":"ONLINE_GATEWAY",
 "https://rootcloud-console.rciot.bekaert.com/frame-cms/api/device/v2/thing/thing-instances?thingType=GATEWAY&_includeMetadata=true&_limit=1&_\
skip=0&_sort=%5B%7B%22field%22%3A%20%22created%22%2C%20%22sortType%22%3A%20%22DESC%22%7D%5D&onlineType=OFFLINE":"OFFLINE_GATEWAY",
 "https://rootcloud-console.rciot.bekaert.com/frame-cms/api/device/v2/thing/thing-instances?thingType=GATEWAY&_includeMetadata=true&_limit=1&_skip=0&_\
sort=%5B%7B%22field%22%3A%20%22created%22%2C%20%22sortType%22%3A%20%22DESC%22%7D%5D&onlineType=NOT_ACTIVE333":"NOT_ACTIVE_GATEWAY"}

url_xpaas_dict = {
    "https://rootcloud-console.rciot.bekaert.com/frame-xpaas/app?&rc_in_wlpaass=true":"xpaas_app_build", 
    "https://rootcloud-console.rciot.bekaert.com/frame-xpaas/compeco/market/componentsStore?&rc_in_wlpaass=true":"xpaas_components", 
    "https://rootcloud-console.rciot.bekaert.com/frame-xpaas/project":"xpaas_data"
}

# 监测URL是否正常响应
def url_check(url):
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
            msg = "%s %s" % (url_xpaas_dict[url], r.status_code)
            print("监测结果: 异常Http状态异常:%s" % r.status_code)
        else:
            # 请求响应正常
            msg_key = url_xpaas_dict[url]
            msg_value = r.status_code
            print("监测结果：正常")
            registry = CollectorRegistry()
            labels = ['req_status','req_method','req_url']
            g_one = Gauge(msg_key,'巡检任务',labels,registry=registry)
            g_one.labels('200','GET', C).set(msg_value)
            #set设定值
            push_to_gateway(
            'https://push-flink.rciot.bekaert.com',
            job = msg_key,
            registry = registry
            )
    except requests.exceptions.ConnectTimeout:
        # 请求响应超时
        msg = "%s请求异常: %s" % (url_xpaas_dict[url], "请求超时", "\n\n")
        print("监测结果：超时")

# 执行URL可用性监测
if __name__ == '__main__':
    # 监控URL可用性
    for i in range(0, len(B)):
        url_check(B[i])