#!/usr/bin/python3

'''
https://www.jb51.net/article/229376.htm#_label0
采用Python requests发起请求监测的URL,检测Http响应状态及是否超时,如果Http状态异常或响应超时,
则通过聚合云推的消息推送API将预警消息发送至邮箱、钉钉机器人、企业微信机器人、微信公众号等,
服务端通过crontab定时(每分钟)执行代码，实现动态监测功能。
'''
import requests
import time
import json

# 监测URL是否正常响应
def url_check(url):
    # 当前时间
    check_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print("开始监测：%s -- %s" % (url, check_time))
    try:
        # 请求URL， 设置3s超时
        r = requests.get(url, timeout=3)
        if r.status_code != 200:
            # 请求响应状态异常
            msg = "监控的URL：%s%sHttp状态异常：%s%s监测时间：%s" % (url, "\n\n", r.status_code, "\n\n", check_time)
            print("监测结果：异常（Http状态异常:%s） -- %s" % (r.status_code, check_time))
            # 通过云推推送消息
            yuntui_push(msg)
        else:
            # 请求响应正常
            print("监测结果：正常 -- %s" % check_time)
    except requests.exceptions.ConnectTimeout:
        # 请求响应超时
        msg = "监控的URL：%s%s请求异常：%s%s监测时间：%s" % (url, "\n\n", "请求超时", "\n\n", check_time)
        print("监测结果：超时 -- %s" % check_time)
        # 通过云推推送消息
        yuntui_push(msg)

# 将预警消息通过云推推送
def yuntui_push(content):
    # 当前时间
    push_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # 云推接口的信息配置，可以通过 https://tui.juhe.cn 自行注册创建
    # (可以配置邮件、钉钉机器人、微信公众号等接收方式)
    token = "*****************"
    service_id = "******"
    title = "URL可用性监控预警"
    doc_type = "markdown"
    body = {"token": token, "service_id": service_id, "title": title, "content": content, "doc_type": doc_type}
    try:
        r = requests.post("https://tui.juhe.cn/api/plus/pushApi", data=body, timeout=15)
        push_res = json.loads(r.content)
        code = push_res['code']
        if code == 200:
            print("推送结果：成功 -- %s" % push_time)
        else:
            print("推送结果：失败（%s） -- %s" % (push_res['reason'], push_time))
    except requests.exceptions.ConnectTimeout:
        print("推送结果：超时 -- %s" % push_time)

# 执行URL可用性监测
if __name__ == '__main__':
    # 监控URL可用性
    # url_check("https://www.test.com")
    url_check("https://www.baidu.com/")

'''
crontab -e
# 每分钟执行一次
*/1 * * * * /usr/bin/python3 /data/check_url/main.py >> /data/log.txt


---------------------------------------------------------------------
cat /data/log.txt
开始监测：https://www.baidu.com/ -- 2021-11-16 15:04:01
监测结果：正常 -- 2021-11-16 15:04:01
开始监测：https://www.baidu.com/ -- 2021-11-16 15:05:02
监测结果：正常 -- 2021-11-16 15:05:02
开始监测：https://www.baidu.com/ -- 2021-11-16 15:06:01
监测结果：正常 -- 2021-11-16 15:06:01
开始监测：https://www.baidu.com/ -- 2021-11-16 15:07:01
监测结果：正常 -- 2021-11-16 15:07:01
开始监测：https://www.baidu.com/ -- 2021-11-16 15:08:01
监测结果：正常 -- 2021-11-16 15:08:01
开始监测：https://www.test.com -- 2021-11-16 15:11:01
监测结果：超时 -- 2021-11-16 15:11:01
推送结果：成功 -- 2021-11-16 15:11:04
开始监测：https://www.test.com -- 2021-11-16 15:12:01
监测结果：超时 -- 2021-11-16 15:12:01
推送结果：成功 -- 2021-11-16 15:12:04

'''