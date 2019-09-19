#coding=utf-8
import requests
from lxml import etree
from scrapy.selector import Selector

def crawl_ips():
    #爬取西刺的免费ip代理
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"}
    ip_list = []
    for i in range(1, 11):
        res = requests.get("http://www.qydaili.com/free/?action=china&page={}".format(i), headers=headers)
        res_html = res.content.decode()
        tree = etree.HTML(res_html)
        tr_list = tree.xpath("//div[@class='container']/table/tbody/tr")[1:]
        print("tr_list: ", tr_list)
        for tr in tr_list:
            ip = tr.xpath("./td[1]/text()")[0]
            port = tr.xpath("./td[2]/text()")[0]
            ip_port = ip + ":" + port
            ip_list.append(ip_port)
    return ip_list

class GetIP(object):

    def __init__(self, ip_list):
        self.ip_list = ip_list

    def judge_ip(self, ip, port):
        #判断ip是否可用
        http_url = "http://www.baidu.com"
        proxy_url = "http://{0}:{1}".format(ip, port)
        try:
            proxy_dict = {
                "http": proxy_url,
            }
            response = requests.get(http_url, proxies=proxy_dict)
        except Exception as e:
            print("无效的ip和端口", proxy_dict["http"])
            return False
        else:
            code = response.status_code
            if code >= 200 and code < 300:
                print("有效ip和端口", proxy_dict["http"])
                self.save_ip_port(proxy_dict["http"])
                return True
            else:
                print("无效的ip和端口", proxy_dict["http"])
                return False

    def run(self):
        for ip_port in self.ip_list:
            ip = ip_port.split(":")[0]
            port = ip_port.split(":")[1]
            self.judge_ip(ip, port)
        self.save_ip_port()

    def save_ip_port(self, ip_port):
        with open("ip_port", "a") as f:
            f.write(ip_port)
            f.write("\n")


# print (crawl_ips())
if __name__ == "__main__":
    ip_list = crawl_ips()
    get_ip = GetIP(ip_list)
    get_ip.run()