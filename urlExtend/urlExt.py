from urlExtend.BaiduUrl import BaiduUrl
import os
from urlExtend.SogouUrl import SogouUrl

class urlExt:
	'''
	扩展url模块入口
	'''
	def __init__(self, out):
		self.target = out+'/subdomain.txt'
		self.out = out + '/url_ext.txt'

	def run(self):
		with open(self.target, 'r') as f:
			lines = f.readlines()
			if not os.path.isfile(self.out):   ##如果文件不存在
				f= open(self.out, 'w+')
				f.close()
			# print(1)
			for domain in lines:
				domain= domain.strip('\n')
				baidu = SogouUrl(domain, self.out)
				baidu.collectUrl()
