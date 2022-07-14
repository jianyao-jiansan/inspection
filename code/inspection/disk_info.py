# -*- coding:utf-8 -*-
# author: guomaoqiu
# desc: 磁盘使用情况统计


# 服务端通过ansible去拿取数据
# ansible all -m shell -a "df -T | grep data"


# [root@node01 ~]# df -T | more
#     0                           1           2         3        4       5    6
# /dev/mapper/data2-data2      ext4     4121732448 65165872 3847170456   2% /data2
# /dev/mapper/data-data        ext4     4121732448 74261092 3838075236   2% /data

import sqlite3
import json
import time

ansible_result_file = "/root/inspection/disk_info.json"
disk_sqlite_db_file = "/root/inspection/disk-sqlite.db"

class DiskUsage():
    print("=" * 18)
    print("数据磁盘时间段内增缩量情况")
    def __init__(self):
        """ 初始化通用配置 """
        # ansible 输出的json文件位置
        # 节点名称
        self.node_name = ""
        # 总计大小
        self.total_size = ""
        # 已用大小
        self.used_size = ""
        # 可用大小
        self.aeach_dataailable_size = ""
        # 使用量百分比
        self.user_percent = ""
        # 挂载点
        self.mounted_on = ""

        #
        self.disk_info_dict = {}
        self.disk_info_list = []

        # flag , 改值定义了数据库的唯一标示
        self.flag = ""

        # 查询的条目数
        self.data_line_num = ""

        # 
        self.db_run_time = ""

        # sqlite初始化:      
        try:
            self.conn = sqlite3.connect(disk_sqlite_db_file)
            self.cursor = self.conn.cursor()
            print("  - 连接数据库成功.")
        except Exception as why:
            print("  - 连接数据库失败.", why)

        # 当前时间，执行此脚本的时间
        str_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        self.current_timestramp = str(time.mktime(time.strptime(str_time, '%Y-%m-%d %H:%M:%S'))).split(".")[0]
        #print("当前时间戳:", self.current_timestramp)

        sql = ''' 
                create  table disk_size (
                    id INTEGER PRIMARY KEY,
                    node_name text,
                    flag text ,
                    total_size BLOB,
                    used_size BLOB,
                    aeach_dataailable_size BLOB,
                    used_percent text,
                    mounted_on text,
                    run_time TIMESTAMP default (datetime('now', 'localtime')),
                    run_timestamp text 
                );
        '''
        try:
            self.cursor.execute(sql)
            print("  - Create table success...")
        except Exception as why:
            print("  - ",why)
            # print("Table already exists...")
    def localtime_to_timestramp(self, localtime):
        """ 本地时间转时间戳 """
        
        # s = time.strftime("%Y-%m-%d %H:%M:%s",localtime)

        return (str(time.mktime(
            time.strptime(localtime, "%Y-%m-%d %H:%M:%S")
        )).split(".")[0])


    def get_json_data(self):
        """ 
        该数据查询获取的是数据单位为KB;
        写入到数据的数据单位是Bytes; 
        """
        with open(ansible_result_file,'r',encoding='utf8') as fp:
            json_data = json.load(fp)
            for k,each_data in  (json_data['plays'][0]['tasks'][0]['hosts']).items():
                for i in (each_data['stdout_lines']):
                    self.flag = str(k) + "_" + (i.split()[6]).strip("/")
                    self.disk_info_list.append({
                            "node_name": k,
                            "flag": self.flag,
                            "total_size": int(i.split()[2]) * 1024,
                            "used_size": int(i.split()[3]) * 1024,
                            "available_size": int(i.split()[4]) * 1024,
                            "used_percent": i.split()[5],
                            "mounted_on": i.split()[6],
                            "run_time": str(each_data['end']).split(".")[0],
                            "run_timestamp": str(self.localtime_to_timestramp(each_data["end"].split('.')[0]))
                        })
        self.data_line_num = len(self.disk_info_list)
        return self.disk_info_list

    def delete_data(self):
        """ 删除15天前的数据 """
        # 当前时间戳 - 15天时间戳
        history_days = int(self.current_timestramp) - 15 * 86400
        results = self.cursor.execute("DELETE FROM disk_size WHERE run_timestamp < '%s';" % history_days )
        all_results  = results.fetchall()
        try:
            self.conn.commit()
            print("  - 删除历史数据成功.")
            print("=" * 18)
        except Exception as why:
            print("  - 删除历史数据失败.", why)
            print("=" * 18)
            self.conn.rollback()

    def _insert_database_table(self):
        for each_data in self.get_json_data():
            self.cursor.execute("INSERT INTO %s VALUES (?,?, ?, ?, ?, ?, ?,?,?,?);" % \
                "disk_size", 
                (
                    None,  
                    each_data["node_name"], 
                    each_data["flag"], 
                    each_data["total_size"], 
                    each_data["used_size"], 
                    each_data["available_size"], 
                    each_data["used_percent"], 
                    each_data["mounted_on"],
                    each_data["run_time"],
                    str(self.localtime_to_timestramp(each_data["run_time"]))
                ))

        try:
            self.conn.commit()
            print("  - 本次统计数据入库成功")
        except Exception as why:
            print("  - 本次统计数据入库失败", why)
            self.conn.rollback()

    def disk_calc(self):
        # 从文件读取到的数据
        for each_file_data in self.get_json_data():
            today_node_name = each_file_data['node_name']
            today_total_size = each_file_data['total_size']
            today_used_size = each_file_data['used_size']
            today_available_size = each_file_data['available_size']
            today_used_percent= each_file_data['used_percent']
            today_mounted_on = each_file_data['mounted_on']
            today_run_time = each_file_data['run_time']
            today_run_timestamp = each_file_data['run_timestamp']
            #print("today_run_timestamp", today_run_timestamp)


            #print("最新获取的 节点 {0} 总大小 {1} Bytes 已经使用: {2} Bytes, 可用: {3} Bytes 挂载点: {4} 使用率: {5} 数据获取时间 {6}".format(
            #today_node_name, today_total_size,today_used_size,today_available_size, today_mounted_on, today_used_percent, today_run_time))

            results =  self.cursor.execute("SELECT * FROM disk_size where flag = '%s' ORDER BY run_timestamp DESC" % each_file_data['flag'] )
            all_results  = results.fetchall()
            
            # 第一次数据库中是没有数据的，所以这里如果第一次执行
            # 为0, 则直接去插入数据
            if len(all_results) == 0:
                self.disk_info_list = []
                self._insert_database_table()

            for happys in all_results:
                db_node_name = happys[1]
                db_flag = happys[2]
                db_total_size = int(happys[3])
                db_used_size = int(happys[4])
                db_available_size = int(happys[5])
                db_used_percent = str(happys[6])
                db_mounted_on = happys[7]
                self.db_run_time = happys[8]
                db_run_timestamp = happys[9]
                #print("db_run_timestamp",db_run_timestamp)   
                try:
                    #print("数据库中的 节点 {0} 总大小 {1} Bytes 已经使用: {2} Bytes, 可用: {3} Bytes 挂载点: {4} 使用率: {5} 数据获取时间 {6}".format(
                    #    db_node_name, db_total_size,db_used_size,db_available_size, db_mounted_on, db_used_percent, db_run_time))
                    #print("相差时间:" ,(int(today_run_timestamp) - int(db_run_timestamp)) / 3600  )  
                    Hours_difference = (int(today_run_timestamp) - int(db_run_timestamp)) / 3600 
                        # 今天-昨天=今天使用量
                    # 本次使用量-上次使用量=相差时间段内使用量
                    increment = (int(today_used_size) - int(db_used_size))
                    increment_M = (int(today_used_size) - int(db_used_size)) / 1024 /1024

                    s = float(str(int(today_available_size) / (int(increment) / float(Hours_difference) * 24 ))[:8])
                    
                    if s < 30:
                        # 预计多久会满=当前剩余量/今天使用量
                        # 如果该值大于0，则说明有增量，否则认为无使用量
                        if increment > 0 :
                            print("    - 节点/数据盘:{0}\n      - {1} 小时({2}分钟)内增量:{3} Bytes({4}M)".format(
                                db_flag,
                                str(Hours_difference)[:6],
                                str(Hours_difference * 60)[:6],
                                increment,
                                increment_M
                            ))   
                            # print(today_available_size, increment)
                            print("      - 预估 {0} 天后耗尽".format(
                                # 当前剩余量 / (  (本次使用量 - 上次使用量) / 本次跟上次相差时间小时数 * 24 )
                                str(int(today_available_size) / (int(increment) / float(Hours_difference) * 24 ))[:8]
                                #str(int(today_available_size) / int(increment)).split(".")[0]
                            ))
                        elif increment == 0:
                            print("    - 节点/数据盘:{0} 今日无增量".format(
                                db_flag
                            ))
                        elif increment < 0:
                            print("    - 节点/数据盘:{0}\n      - {1} 小时({2}分钟)内缩量:{3} Bytes({4}M)".format(
                                db_flag,
                                str(Hours_difference)[:6],
                                str(Hours_difference * 60)[:6],
                                increment,
                                increment_M
                            ))
                            print("      - 今日缩量，大小为: {0} Bytes({1}M).".format(increment, increment_M))
                        else:
                            pass
                except Exception as why:
                    print("计算出错:", why)
                break

        print("  - 本次获取时间:{0}\n  - 上次获取时间:{1}".format(today_run_time ,self.db_run_time))

        #对比完成后插入新的数据
        try:
            # 重置从文件中读取的最新的内容列表为空
            # 因为上面已经执行了get_json_data 函数
            # 会出现重复的内容
            self.disk_info_list = []
            # 测试判断拿取的数据是不是旧数据
            # 如果是旧数据就不需要再次入库
            if Hours_difference != 0:
                self._insert_database_table()
                print("  - 更新数据成功.")
            else:
                print("  - 无最新数据.")
        except:
            print("  - 更新数据失败.")
        # 删除历史数据：
        self.delete_data()

# 计算
# DiskUsage().disk_calc()