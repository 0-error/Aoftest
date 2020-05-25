import threading
import config_aoftest
from config_aoftest import logger
import queue
import json
import os
import requests
import subprocess
import time

class craw:
    '''
    爬虫调用模块
    '''

    def __init__(self, target, out, file_url):
        self.target = target
        self.out = out
        self.file_url = file_url
        self.urls_queue = queue.Queue() #异步请求队列

    def craw(self):
        '''启动爬虫'''
        file = open(self.out+self.file_url, 'r')
        f = open(self.out+'/request.txt', 'a')
        for line in file.readlines():
            line = line.strip('\n')
            logger.log('INFOR', '[+]'+':开始爬虫%s' % line)
            cmd = config_aoftest.craw_cmd
            # print(cmd)
            cmd.append(line)
            rsp = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # print("before")
            try:
                output, error = rsp.communicate(timeout=config_aoftest.craw_timeout)
            except subprocess.TimeoutExpired:
                logger.log('ERROR', "[-]爬虫超时")
                rsp.kill()
                continue
           # print("after")
            try:
                result = json.loads(output.decode().split("--[Mission Complete]--")[1])
            except:
                logger.log('ERROR', '[-]爬虫json解析错误')
                continue
            req_list = result["req_list"]
            sub_domain = result["sub_domain_list"]
            logger.log('INFOR', "[+][crawl ok]\n")
            if req_list:
                for req in req_list:
                    f.write(req['url']+'\n')
            else:
                logger.log('ERROR', "[-]req_list不存在\n")
                continue
            time.sleep(config_aoftest.craw_sleep)
        f.close()
        file.close()

    def craw_thread(self):
        '''
        多线程爬虫
        '''
        t = threading.Thread(target=request)
        t.start()
        file = open(self.out+file_url, 'r')
        f = open(self.out+'/request.txt', 'a')
        for line in file.readlines():
            line = line.strip('\n')
            logger.log('INFOR', '[+]开始爬虫%s' % line)
            cmd = config_aoftest.craw_thread_cmd
            cmd.append(line)
            rsp = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            try:
                output, error = rsp.communicate(timeout=config_aoftest.craw_timeout)
            except subprocess.TimeoutExpired:
                logger.log('ERROR', "[-]爬虫超时")
                rsp.kill()
                continue
            try:
                result = json.loads(output.decode().split("--[Mission Complete]--")[1])
            except:
                logger.log('ERROR', '[-]爬虫json解析错误')
                continue
            req_list = result["req_list"]
            sub_domain = result["sub_domain_list"]
            logger.log('INFOR', "[+][crawl ok]\n")
            if req_list:
                for req in req_list:
                    f.write(req['url']+'\n')
                    self.urls_queue.put(req)
            else:
                logger.log('ERROR', "[-]req_list不存在\n")
                continue 
            time.sleep(config_aoftest.craw_thread_sleep)
        f.close()
        file.close()

    def craw_alone(self):
        '''
        单独爬虫模块
        '''
        file = open(self.target, 'r')
        if not os.path.exists(self.out):                   #判断是否存在文件夹如果不存在则创建为文件>夹
            os.makedirs(self.out)            #makedirs 创建文件时如果路径不存在会创建这个路径
            logger.log('INFOR', "new folder... ")
        else:
            logger.log('INFOR', "There is this folder!")
        f = open(self.out+'/request.txt', 'a')
        for line in file.readlines():
            line = line.strip('\n')
            logger.log('INFOR', '[+]开始爬虫%s' % line)
            cmd = config_aoftest.craw_cmd
            # print(cmd)
            cmd.append(line)
            rsp = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # print("before")
            try:
                output, error = rsp.communicate(timeout=config_aoftest.craw_timeout)
            except subprocess.TimeoutExpired:
                logger.log('ERROR', "[-]爬虫超时")
                rsp.kill()
                continue
            # print("after")
            try:
                result = json.loads(output.decode().split("--[Mission Complete]--")[1])
            except:
                logger.log('ERROR', '[-]爬虫json解析错误')
                continue
            req_list = result["req_list"]
            sub_domain = result["sub_domain_list"]
            logger.log('INFOR', "[+][crawl ok]\n")
            if req_list:
                for req in req_list:
                    f.write(req['url']+'\n')
            else:
                logger.log('ERROR', "[-]req_list不存在\n")
                continue
            time.sleep(config_aoftest.craw_sleep)
        f.close()
        file.close()

    def craw_alone_thread(self):
        '''
        多线程单独爬虫模块
        '''
        t = threading.Thread(target=request)
        t.start()
        file = open(self.target, 'r')
        if not os.path.exists(self.out):                   #判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(self.out)            #makedirs 创建文件时如果路径不存在会创建这个路径
            logger.log('INFOR', "new folder...")
        else:
            logger.log('INFOR', "There is this folder!")
        f = open(target2+'/request.txt', 'a')
        for line in file.readlines():
            line = line.strip('\n')
            logger.log('INFOR', '[+]开始爬虫%s' % line)
            cmd = config_aoftest.craw_thread_cmd
            cmd.append(line)
            rsp = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            try:
                output, error = rsp.communicate(timeout=config_aoftest.craw_timeout)
            except subprocess.TimeoutExpired:
                logger.log('ERROR', "[-]爬虫超时")
                rsp.kill()
                continue
            try:
                result = json.loads(output.decode().split("--[Mission Complete]--")[1])
            except:
                logger.log('ERROR', '爬虫json解析错误')
                continue
            req_list = result["req_list"]
            sub_domain = result["sub_domain_list"]
            logger.log('INFOR', "[+][crawl ok]")
            if req_list:
                for req in req_list:
                    f.write(req['url']+'\n')
                    self.urls_queue.put(req)
            else:
                logger.log('ERROR', "[-]req_list不存在\n")
                continue
            time.sleep(config_aoftest.craw_thread_sleep)
        f.close()
        file.close()

    def request(self):
        while True:
            # if(urls_queue.empty() == False:
            if(self.urls_queue.qsize()==0):
                time.sleep(config_aoftest.queue_request_sleep)
            # print(urls_queue.qsize())
            req = self.urls_queue.get()
            proxies = {
            'http': 'http://'+config_aoftest.proxy,
            'https': 'http://'+config_aoftest.proxy,
            }
            urls0 =req['url']
            headers0 =req['headers']
            method0=req['method']
            # print(method0)
            data0=req['data']
            if method0 == 'GET':
                try:
                    a = requests.get(urls0, headers=headers0, proxies=proxies,timeout=15,verify=False)
                    # time.sleep(0.5)
                except:
                    # print('get错误')
                    pass
            elif method0 == 'POST':
                try:
                    requests.post(urls0, headers=headers0,data=data0, proxies=proxies,timeout=15,verify=False)
                    # time.sleep(0.5)
                except:
                    # print('post错误')
                    pass
            else:
                logger.log('ALERT', '[-]存在其他HTTP方法请求，xray不支持')