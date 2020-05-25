#coding: utf-8
import requests
from bs4 import BeautifulSoup as bs
import re
from queue import Queue
from argparse import ArgumentParser
from config_aoftest import logger



class SogouUrl:
    '''
    百度搜集url模块
    '''
    def __init__(self,domain,file):
        self.domain = domain
        self.keyword = 'site:'+domain
        self.limit_num = 10
        self.writePath = file
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}

    def collectUrl(self):
        page_num = 0
        while True:
            url = 'https://www.sogou.com/web?query=' + self.keyword + '&page=' + str(page_num) 
            page_num = page_num+1
            try:
                resp = requests.get(url, headers=self.headers, timeout=6) #得到url返回的搜索列表，包含10个值
                # print(resp.text)
                soup = bs(resp.text, features="html.parser")
                bqs = soup.find_all(name='a', attrs={'name':'dttl'})
                if len(bqs):
                    for bq in bqs:
                        href = 'https://www.sogou.com'+bq['href']
                        r = requests.get(href, headers=self.headers, timeout=3)
                        if r.status_code == 200:
                            p1 = re.compile(r'[(]\"(.*?)\"[)]', re.S)
                            url = re.findall(p1, r.text)
                            logger.log('INFOR', '[+]搜狗url扩展:%s' % url[0])
                            with open(self.writePath, 'r') as f: 
                                s = url[0] +'\n'
                                fs = f.read()
                                if self.checkrepeat(s, fs):
                                    continue
                            with open(self.writePath, 'a') as f:
                                f.write(url[0] + '\n')
                else:
                    logger.log('INFOR','[-]搜狗搜索无响应')                                                      ##若返回列表为空，则只记录原始域名
                    with open(self.writePath, 'a') as f:
                        f.write('http://'+self.domain + '\n') 
                if '<a id="sogou_next"' not in resp.text:
                    # print('out') 
                    break
            except Exception as e:
                print(e)
                with open(self.writePath, 'a') as f:
                    f.write('http://'+self.domain + '\n')
                break
            if page_num*10 >= self.limit_num:  # 搜索条数限制
                break

    def checkrepeat(self, s, fs):   ## 查看url是否重复
        # print(s)
        if s in fs:
            logger.log('INFOR', '[-]搜狗url扩展重复')
            return True
        else:
            return False


if __name__ == '__main__':
    sogou = SogouUrl('spdb.com.cn','/baidu')
    sogou.collectUrl()