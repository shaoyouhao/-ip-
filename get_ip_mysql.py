

import requests
import parsel
import pymysql

conn = pymysql.connect(host="127.0.0.1", user="root", password="123456", db="ips")
cursor = conn.cursor()
"""
    该代码是获取66免费代理网站：http://www.66ip.cn/1.html的所有ip地址，并
    将ip地址及其他信息保存到数据库中
        
        author：邵尤豪
"""
def crawl_ips(url):
    header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
    }
    response = requests.get(url=url, headers=header)
    response.encoding = 'gbk'
    html = parsel.Selector(response.text)
    trs = html.xpath("//div[@align='center']/table//tr")[1:]
    for tr in trs:
        ip = tr.xpath("./td[1]/text()").get()
        port = tr.xpath("./td[2]/text()").get()
        address = tr.xpath("./td[3]/text()").get()
        proxy_type = tr.xpath("./td[4]/text()").get().replace("代理","")
        date_time = tr.xpath("./td[5]/text()").get().replace("验证","")
        date_time = date_time
        cursor.execute(
            f"insert into ip_pool(ip,port,address,proxy_type,date_time) \
            VALUES('{ip}' ,'{port}' ,'{address}' ,'{proxy_type}' ,'{date_time}' )"
        )
        conn.commit()
        # ip_list.append((ip, port, address, type, date))
        print(ip,port, address,proxy_type,date_time)


def run():
    for i in range(3, 30):
        url = "http://www.66ip.cn/{}.html".format(i)
        print(url)
        crawl_ips(url)
run()
conn.close()
cursor.close()








