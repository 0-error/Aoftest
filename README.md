# Aoftest

**Aoftest是一款自动化资产收集和漏洞发现工具**


Aoftest是一个集合域名发现，ip发现，端口扫描，漏洞发现的自动化渗透测试工具。
该工具结合oneforall，crawlergo，xray，nmap等开源软件进行开发。分为onforall子域发现模块，statistic分析模块，crawlergo爬虫模块，nmap端口扫描模块，xray漏洞扫描模块，url扩展模块。

整体思想为，利用oneforall进行子域发现，statistic模块对发现结果进行分析，提取ip，可访问链接等信息，urlextend模块利用搜索引擎扩展url，再利用crawlergo爬虫对结果url进行爬虫，将xray设置为被动监听模式，爬虫请求将交给xray进行漏洞发现处理，最后再利用nmap对收集到的ip进行端口扫描。

漏洞的发现成果一是在于覆盖检测面，二是漏洞检测能力。开发该工具的初衷在于将该过程自动化，包括信息收集，包括爬虫，漏洞检测过程，并且需要灵活变化和配置，所以结合现有的比较好用的轮子，造了该轮子。


## 使用方法

**本项目基于几个已知轮子，oneforall（https://github.com/shmilylty/OneForAll）, crawlergo(https://github.com/0Kee-Team/crawlergo), xray(https://github.com/chaitin/xray)**
**该项目基于python3.8**，建议使用python虚拟环境，使用方法：

```
pip install requirements.txt
```

运行xray被动扫描模块, xray配置可参考 https://github.com/chaitin/xray

```
./xray_darwin_amd64 webscan --listen 127.0.0.1:7777 --html-output __datetime__.html
```

下载Chromium并在配置文件中进行配置

输入并保存域名（以某厂商之前的src为例）：

![](https://github.com/0-error/picture/blob/master/domain.png)

运行程序

```
python aoftest.py --target=[域名文件] --out=[输出文件夹] run
```
<img src="https://github.com/0-error/picture/blob/master/yunxing.png" height="280" width="600">

**运行结果**

输出文件夹下，subdomain信息：

<img src="https://github.com/0-error/picture/blob/master/subdomain.png" height="280" width="600">

ip信息：

<img src="https://github.com/0-error/picture/blob/master/ip.png" height="280" width="600">

url信息：

<img src="https://github.com/0-error/picture/blob/master/url.png" height="280" width="600">

爬虫请求信息：

<img src="https://github.com/0-error/picture/blob/master/request.png" height="280" width="600">

漏洞信息：

<img src="https://github.com/0-error/picture/blob/master/vuln.png" height="280" width="600">



## 其他用法

**各模块可独立使用**

配置文件更改

<img src="https://github.com/0-error/picture/blob/master/peizhi1.png" height="280" width="600">

可在资产已知的情况对资产进行爬虫和扫描

配置文件更改

<img src="https://github.com/0-error/picture/blob/master/peizhi2.png" height="280" width="600">

可单独运行资产收集，不进行爬虫和扫描

配置代理，可与burp联动

<img src="https://github.com/0-error/picture/blob/master/peizhi3.png" height="280" width="600">

更多用法可以学习oneforall，crawlergo，xray研究。
