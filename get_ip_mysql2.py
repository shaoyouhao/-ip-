
import requests
import parsel
import pymysql

conn = pymysql.connect(host="127.0.0.1", user="root", password="123456", db="ips",charset="utf8")
cursor = conn.cursor()
"""
    该代码是获取西刺免费代理网站：https://www.xicidaili.com/nn/的所有ip地址，并
    将ip地址及其他信息保存到数据库中

        author：邵尤豪
"""
def crawl_ips(url):
    header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
    }
    response = requests.get(url=url, headers=header)
    # response.encoding = 'gbk'
    html = parsel.Selector(response.text)
    trs = html.xpath("//table[@id='ip_list']//tr")[1:]
    for tr in trs:
        ip = tr.xpath("./td[2]/text()").get()
        port = tr.xpath("./td[3]/text()").get()
        address = tr.xpath("./td[5]/text()").get()
        proxy_type = tr.xpath("./td[6]/text()").get()
        date_time = tr.xpath("./td[10]/text()").get()
        print(ip,port,address,proxy_type,date_time)
        cursor.execute(
            f"insert into ip_pool(ip,port,address,proxy_type,date_time) \
            VALUES('{ip}' ,'{port}' ,'{address}' ,'{proxy_type}' ,'{date_time}' )"
        )
        conn.commit()
        # ip_list.append((ip, port, address, type, date))
        print(ip ,port, address ,proxy_type ,date_time)


def run():
    for i in range(3, 30):
        url = f"https://www.xicidaili.com/nn/{i}"
        # print(url)
        crawl_ips(url)
run()
conn.close()
cursor.close()

# CREATE TABLE `ip_new` (
#   `id` int(10) NOT NULL AUTO_INCREMENT,
#   `ip` varchar(30) NOT NULL unique,
#   `port` char(10) NOT NULL,
#   `niming` varchar(10) DEFAULT NULL,
#   `proxy_type` varchar(10)  DEFAULT NULL,
#   `date_time` varchar(30) DEFAULT NULL,
#   PRIMARY KEY (`id`)
# );





