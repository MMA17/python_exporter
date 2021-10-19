from datetime import datetime
from os import stat
import pytz
import re
import pandas as pd
import time
from prometheus_client import start_http_server, Summary, Gauge
import crawler
import time
from prometheus_client import start_http_server, Summary, Gauge

def parse_str(x):
    return x[1:-1]

def parse_datetime(x):
    dt = datetime.strptime(x[1:-7], '%d/%b/%Y:%H:%M:%S')
    dt_tz = int(x[-6:-3])*60+int(x[-3:-1])
    return dt.replace(tzinfo=pytz.FixedOffset(dt_tz))

data = pd.read_csv(
    'access.log',
    sep=r'\s(?=(?:[^"]*"[^"]*")*[^"]*$)(?![^\[]*\])',
    engine='python',
    na_values='-',
    header=None,
    usecols=[0, 3, 4, 5, 6, 7, 8],
    names=['ip', 'time', 'request', 'status', 'size', 'referer', 'user_agent'],
    converters={
                    'time': parse_datetime,
                    'request': parse_str,
                    'status': int,
                    'size': int,
                    'referer': parse_str,
                    'user_agent': parse_str})

total_req = Gauge('total_requset', 'Total request to HTTP Server')
def get_total_req():
    print("Total requests: " + str(data.count(axis='columns').count()))
    
    total_req.set(data.count(axis='columns').count())

def get_num_success_req():
    data_success = data[data['status'] == 200]
    print("Success requests: " + str(data_success.count(axis='columns').count()))

def get_num_error_req():
    data_error_400 = data[data['status'] == 400]
    data_error_401 = data[data['status'] == 401]
    data_error_402 = data[data['status'] == 402]
    data_error_403 = data[data['status'] == 403]
    data_error_404 = data[data['status'] == 404]
    print("Error requests: " + str(data_error_400.count(axis='columns').count() + data_error_401.count(axis='columns').count() 
                            + data_error_402.count(axis='columns').count() +  data_error_403.count(axis='columns').count() 
                            + data_error_404.count(axis='columns').count()))
# print(data.head(9999))

