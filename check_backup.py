#! -*- coding:utf-8 -*-
# author: guomaoqiu
# date: 2022-04-20
# desc: 检查备份文件是是否正常

import os
import glob
import time


_mysql="/data/db-backup/mysql-backup-data/*"
_mongo="/data/db-backup/mongo-backup-data/*"
_pgsql="/data/db-backup/postgresql-backup-data/postgresql-clm/*"

current_time_day = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())).split(" ")[0]


size = None

# 单独获取目录的大小
def get_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    total_size = total_size / 1024 / 1024
    #print(total_size)
    return total_size

def check(db_type, name):
    # 查找出最新生成的文件
    #print(db_type)
    new_file = (max(glob.glob(db_type), key=os.path.getmtime))
    
    file_stat=os.stat(new_file)
    mtime = file_stat.st_mtime
    size = file_stat.st_size / 1024 /1024 
    backup_file_name = os.path.basename(new_file)
    #print(backup_file_name)
    # 判断文件是目录还是一个压缩包
    if os.path.isdir(new_file):
        #print("is dir")
        size = get_size(new_file)
        #print(size)
    elif os.path.isfile(new_file):
        #print("is file")
        size = size
        #print(size)
    else:
        pass

    if size > 10 and current_time_day in backup_file_name:
        #print(name)
        #print({name: True })
        print("{0} {1} Backup Success!".format(current_time_day,name))
        #print({name: True })
    else:
        #print({name: False })
        print("{0} {1} Backup Failed!({2})".format(current_time_day ,name,new_file))
print("==================")
check(_mysql, name="mysql")
check(_mongo, name="mongo")
check(_pgsql, name="pgsql")
print("==================")
