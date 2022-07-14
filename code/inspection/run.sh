#!/bin/sh


# 如果第一次成功，就按最新的log发送
> /tmp/inspection.log
echo "inspection start..."
python3 main.py >> /tmp/inspection.log

echo "发送消息..."
python3 send_inspection_info.py

echo "发送至巡检展示平台"
python3 send_to_web.py
