import nmap
import config_aoftest
from config_aoftest import logger

class nmapScan:
    '''
    nmap扫描模块
    '''
    def __init__(self, out):
        self.out = out

    def nmapscan(self):
        nm = nmap.PortScanner()
        logger.log('INFOR', '[+]开始nmap扫描')
        nm.scan('None',None,config_aoftest.nmap_cmd+self.out+'/ip.txt')
        with open(out+'/nmap.xml', 'w', encoding='utf-8') as file:
            file.write(nm.get_nmap_last_output())
        logger.log('INFOR', '[+]结束nmap扫描')