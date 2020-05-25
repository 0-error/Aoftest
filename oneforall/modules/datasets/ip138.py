from common.query import Query


class IP138(Query):
    def __init__(self, domain):
        Query.__init__(self)
        self.domain = self.register(domain)
        self.module = 'Dataset'
        self.source = 'IP138Query'
        self.addr = 'https://site.ip138.com/{domain}/domain.htm'

    def query(self):
        """
        向接口查询子域并做子域匹配
        """
        self.header = self.get_header()
        self.proxy = self.get_proxy(self.source)
        self.addr = self.addr.format(domain=self.domain)
        resp = self.get(self.addr)
        if not resp:
            return
        subdomains = self.match(self.domain, resp.text)
        # 合并搜索子域名搜索结果
        self.subdomains = self.subdomains.union(subdomains)

    def run(self):
        """
        类执行入口
        """
        self.begin()
        self.query()
        self.finish()
        self.save_json()
        self.gen_result()
        self.save_db()


def do(domain):  # 统一入口名字 方便多线程调用
    """
    类统一调用入口

    :param str domain: 域名
    """
    query = IP138(domain)
    query.run()


if __name__ == '__main__':
    do('example.com')
