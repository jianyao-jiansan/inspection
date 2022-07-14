

import time

current_time_hours = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())).split(" ")[1].split(":")[0]






if current_time_hours != "19":
    exit()