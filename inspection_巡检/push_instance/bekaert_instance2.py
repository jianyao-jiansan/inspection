# coding=utf-8

from prometheus_client import CollectorRegistry,Gauge,push_to_gateway



if __name__ == '__main__':
    registry=CollectorRegistry()
    labels= ['req_status','req_method','req_url']
    g_one=Gauge('requests_total','url请求次数',labels,registry=registry)
    g_two=Gauge('avg_response_time_seconds','1分钟内的URL平均响应时间',labels,registry=registry)
    g_one.labels('200','GET','/test/url').set(1)
    #set设定值
    g_two.labels('200','GET','/test/api/url/').set(10)
    #set设定值
    push_to_gateway(
        'https://push-flink.rciot.bekaert.com',
        job='test999',
        registry=registry
    )