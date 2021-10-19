import time
# from typing import Counter
from prometheus_client import start_http_server, Summary, Gauge, Counter
from datetime import datetime
from os import stat
import pytz
import re
import pandas as pd
import time
from prometheus_client import start_http_server, Summary, Gauge

# def parse_str(x):
#     return x[1:-1]

# def parse_datetime(x):
#     dt = datetime.strptime(x[1:-7], '%d/%b/%Y:%H:%M:%S')
#     dt_tz = int(x[-6:-3])*60+int(x[-3:-1])
#     return dt.replace(tzinfo=pytz.FixedOffset(dt_tz))

total_req = Counter('total_requset', 'Total number of request to HTTP Server')
def get_total_req():
    # print("Total requests: " + str(data.count(axis='columns').count()))
    total_req.inc(data.count(axis='columns').count())

num_req_success = Gauge('Num_req_success', 'Number of requests success to HTTP Server',labelnames=['code'])
def get_num_success_req():
    data_success = data[data['status'] == 200]
    # print("Success requests: " + str(data_success.count(axis='columns').count()))
    num_req_success.labels('200').set(data_success.count(axis='columns').count())

num_req_error = Gauge('Num_req_error', 'Number of requests error to HTTP Server', labelnames=['code'])
def get_num_error_req():
    data_error_400 = data[data['status'] == 400]
    data_error_401 = data[data['status'] == 401]
    data_error_402 = data[data['status'] == 402]
    data_error_403 = data[data['status'] == 403]
    data_error_404 = data[data['status'] == 404]
    num_req_error.labels('400').set(data_error_400.count(axis='columns').count())
    num_req_error.labels('401').set(data_error_401.count(axis='columns').count())
    num_req_error.labels('402').set(data_error_402.count(axis='columns').count())
    num_req_error.labels('403').set(data_error_403.count(axis='columns').count())
    num_req_error.labels('404').set(data_error_404.count(axis='columns').count())

num_req_persec = Gauge('Num_req_persec', 'Number of requests to HTTP Server per second')
def get_req_per_sec():
    num_req_persec.set(data.count(axis='columns').count())

if __name__ == '__main__':
    f = open('/var/log/apache2/access.log', 'r')
    start_http_server(8000)
    while True:
        lines = f.readlines()
        if (lines != ""):
            w = open('temp.log', 'w')
            w.writelines(lines)
            w.close()
            # print (f.tell())
            data = pd.read_csv(
            'temp.log',
            sep=r'\s(?=(?:[^"]*"[^"]*")*[^"]*$)(?![^\[]*\])',
            engine='python',
            na_values='-',
            header=None,
            usecols=[0, 3, 4, 5, 6, 7, 8],
            names=['ip', 'time', 'request', 'status', 'size', 'referer', 'user_agent'],
            converters={
                            'time': str,
                            'request': str,
                            'status': int,
                            'size': str,
                            'referer': str,
                            'user_agent': str})

            get_req_per_sec()
            get_total_req()
            get_num_success_req()
            get_num_error_req()
        # print(data.head(9999))
        time.sleep(15)
        