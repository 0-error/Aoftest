#coding: utf-8
import requests
from bs4 import BeautifulSoup as bs
import re
from queue import Queue
from argparse import ArgumentParser
from config_aoftest import logger

class BaiduUrl:
    '''
    百度搜集url模块
    '''
    def __init__(self,domain,file):
        self.domain = domain
        self.keyword = 'site:'+domain
        self.limit_num = 10
        self.writePath = file
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
        # self.headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'}

    def collectUrl(self):
        page_num = 0
        while True:
            url = 'https://www.baidu.com/s?wd=' + self.keyword + '&pn=' + str(page_num) 
            page_num = page_num+10
            try:
                resp = requests.get(url, headers=self.headers, timeout=6) #得到url返回的搜索列表，包含10个值
                # print(resp.text)
                soup = bs(resp.text, features="html.parser")
                bqs = soup.find_all(name='a', attrs={'data-click':re.compile(r'.'), 'class':None})
                # print(bqs)
                if len(bqs):
                    for bq in bqs:
                        r = requests.get(bq['href'], headers=self.headers, timeout=3)
                        if r.status_code == 200:
                            logger.log('INFOR', '[+]百度url扩展:%s' % r.url)
                            with open(self.writePath, 'r') as f: 
                                s = r.url +'\n'
                                fs = f.read()
                                if self.checkrepeat(s, fs):
                                    continue
                            with open(self.writePath, 'a') as f:
                                f.write(r.url +'\n')
                else:
                    logger.log('INFOR','[-]百度搜索无响应')                                                      ##若返回列表为空，则只记录原始域名
                    with open(self.writePath, 'a') as f:
                        f.write('http://'+self.domain + '\n') 
                if '&pn={next_pn}&'.format(next_pn=page_num) not in resp.text:
                    # print(out)
                    break
            except Exception as e:             ##捕获到错误，记录原始域名并跳出循环
                print(e)
                with open(self.writePath, 'a') as f:
                    f.write('http://'+self.domain + '\n')
                break
            if page_num >= self.limit_num:  # 搜索条数限制
                break

    def checkrepeat(self, s, fs):   ## 查看url是否重复
        # print(s)
        if s in fs:
            logger.log('INFOR', '[-]百度url扩展重复')
            return True
        else:
            return False


if __name__ == '__main__':
    baidu = BaiduUrl('spdb.com.cn','/baidu')
    baidu.collectUrl()