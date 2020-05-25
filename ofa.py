import config_aoftest 
import sys
sys.path.append(config_aoftest.oneforall_path)

from config_aoftest import logger
from oneforall.oneforall import OneForAll
import pathlib
import json
import os
import re

class ofa:
    '''
    oneforall分析模块
    '''
    def __init__(self, target, out):
        self.target = target
        self.out = out

    def ofa(self):
        f = open(self.target,'r')
        folder = self.out
        if not os.path.exists(folder):                   #判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(folder)            #makedirs 创建文件时如果路径不存在会创建这个路径
            logger.log('INFOR', "new folder")
        else:
            logger.log('INFOR', "There is this folder!")
        lines = f.readlines()
        for domain in lines:
            domain = domain.strip('\n')
            OneForAll(target=domain, alive=True, format='json').run()
        f.close()

    def statistic(self):
        f = open(self.target,'r')
        f1 = open(self.out+'/subdomain.txt', 'a')
        f2 = open(self.out+'/ip.txt', 'a')
        f3 = open(self.out+'/url.txt','a')
        lines = f.readlines()
        for domain in lines:
            domain = domain.strip('\n')
            sub_file = pathlib.Path(__file__).parent.resolve().joinpath('oneforall/results', domain + '.json')
            if not sub_file.is_file():
                logger.log('ALERT',  '[-]子域名文件：%s未发现' % sub_file)
                continue
            with open(sub_file, 'r', encoding='utf-8') as file:
                tmp_str = file.read()
            try:
                tmp_dict = json.loads(tmp_str)
            except:
                logger.log('ERROR',  '[-]子域名文件:%s解析json格式错误' % sub_file)
                continue
            tmp_ip = list()
            for subdomain_dict in tmp_dict:
                subdomain = subdomain_dict['subdomain']  # 取子域名
                f1.write(subdomain+'\n')
                url = subdomain_dict['url']
                f3.write(url+'\n')
                status = subdomain_dict['status']
                if status is not None:      
                    ip_str = subdomain_dict['content']
                    ip_list = ip_str.split(',')
                    for ip in ip_list:
                        if self.checkip(ip):
                            logger.log('INFOR', '[-]ip%s invaild' % ip)
                            continue
                        if self.checkrepeat(ip,tmp_ip):  #如果检查出ip已存在，将不记录ip表中
                            logger.log('INFOR', '[-]ip%s 已存在' % ip)
                            continue
                        f2.write(ip+'\n')
                        tmp_ip.append(ip)
        f.close()
        f1.close()
        f2.close()
        f3.close()

    def checkrepeat(self, ip, tmp_ip):
        '''检查是否重复字符'''
        for tmp in tmp_ip:
            if ip == tmp:
                logger.log('INFOR', '[-]%s检查重复' % ip)
                return True
        return False

    def checkip(self, ip):
        if re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", ip):
            return False
        else:
            return True

