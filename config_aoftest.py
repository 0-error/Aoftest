# coding=utf-8
import os
from loguru import logger
import json

oneforall_path = '/Users/mac/Documents/渗透工具/aoftest/oneforall'

##代理配置
proxy = '127.0.0.1:7777'

#爬虫配置
headers = {
    "Cookie":"security=low; security_level=0; PHPSESSID=d6c6c1337189cb6d2497b4a346bc235f"
}
k = "logout"

# craw_cmd = ["./crawlergo", "-c", "Chromium.app/Contents/MacOS/Chromium", "-o", "json", "-f", "smart", "-t", "20", "-m", "500", "--push-to-proxy", proxy, "--push-pool-max", "10"]
craw_cmd = ["./crawlergo", "-c", "Chromium.app/Contents/MacOS/Chromium", "-o", "json", "-f", "smart", "-t", "20", "-m", "500", "--fuzz-path", "--push-to-proxy", proxy, "--push-pool-max", "10"]
# craw_cmd = ["./crawlergo", "-c", "Chromium.app/Contents/MacOS/Chromium", "-o", "json", "-f", "smart", "-t", "20", "-m", "500", "--custom-headers", json.dumps(headers), "--push-to-proxy", proxy, "--push-pool-max", "10"]
# craw_cmd = ["./crawlergo", "-c", "Chromium.app/Contents/MacOS/Chromium", "-o", "json", "--ignore-url-keywords", k, "-f", "smart", "-t", "20", "-m", "400", "--custom-headers", json.dumps(headers), "--push-to-proxy", "http://127.0.0.1:8080", "--push-pool-max", "10"]
craw_thread_cmd = ["./crawlergo", "-c", "Chromium.app/Contents/MacOS/Chromium", "-o", "json", "-f", "smart", '-t', '15', '-m', '400']
craw_sleep = 6
craw_thread_sleep = 4
craw_thread = False
queue_request_sleep = 4
craw_timeout =480

#nmap配置
nmap_cmd = '-sC -sS --min-rate 800 -i'

#模块配置
enable_all_module = False  # 启用所有模块
craw_alone = True
#enable_partial_module = ['ofa', 'ipcheck', 'craw', 'nmapscan']
# enable_partial_module = ['ofa', 'ipcheck', 'urlExtend', 'craw', 'nmapscan']
enable_partial_module = ['urlExtend', 'craw', 'nmapscan']
# enable_partial_module = ['ipcheck','urlExtend', 'craw', 'nmapscan']
# enable_partial_module = ['ipcheck', 'craw', 'nmapscan']
#enable_partial_module = ['craw', 'nmapscan']

## 日志配置
logger.level(name='TRACE', no=5, color='<cyan><bold>', icon='✏️')
logger.level(name='DEBUG', no=10, color='<blue><bold>', icon='🐞 ')
logger.level(name='INFOR', no=20, color='<green><bold>', icon='ℹ️')
logger.level(name='ALERT', no=30, color='<yellow><bold>', icon='⚠️')
logger.level(name='ERROR', no=40, color='<red><bold>', icon='❌️')
logger.level(name='FATAL', no=50, color='<RED><bold>', icon='☠️')

if not os.environ.get('PYTHONIOENCODING'):  # 设置编码
    os.environ['PYTHONIOENCODING'] = 'utf-8'