import fire
import config_aoftest 
from ofa import ofa
from craw import craw
from nmapScan import nmapScan
from urlExtend.urlExt import urlExt

class aoftest:
    def __init__(self, target, out):
        self.target = target
        self.out = out

    def run(self):
        '''
        入口函数
        '''
        ofaIns = ofa(self.target, self.out)
        if 'urlExtend' in config_aoftest.enable_partial_module:  ##若存在urlExtend模块，则爬虫读取的文件为url_ext.txt
            crawIns = craw(self.target, self.out, '/url_ext.txt')
        else:
            crawIns = craw(self.target, self.out, '/url.txt')
        nmapScanIns = nmapScan(self.out)
        urlExtIns = urlExt(self.out)
        if config_aoftest.enable_all_module:
            ofaIns.ofa()
            ofaIns.statistic()
            urlExtIns.run()
            if config_aoftest.craw_thread:
                crawIns.craw_thread()
            else:
                crawIns.craw()
            nmapScanIns.nmapscan()
        elif config_aoftest.craw_alone:
            if config_aoftest.craw_thread:
                crawIns.craw_alone_thread()
            else:
                crawIns.craw_alone()
        else:
            if 'ofa' in config_aoftest.enable_partial_module:
                ofaIns.ofa()
            if 'ipcheck' in config_aoftest.enable_partial_module:
                ofaIns.statistic()
            if 'urlExtend' in config_aoftest.enable_partial_module:
                urlExtIns.run()
            if 'craw' in config_aoftest.enable_partial_module:
                if config_aoftest.craw_thread:
                    crawIns.craw_thread()
                else:    
                    crawIns.craw()
            if 'nmapscan' in config_aoftest.enable_partial_module:
                nmapScanIns.nmapscan()
        

if __name__ == '__main__':
    print('\n----AofTest是一款自动化资产收集和漏洞发现系统----\n')
    print('----Start AofTest----\n')
    fire.Fire(aoftest)