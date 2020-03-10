import pymysql
import requests




class GetIP(object):

    def __init__(self):
        self.conn = pymysql.connect(host="127.0.0.1",user="root",password="123456", \
                                    db="ips",charset="utf8"
                                    )
        self.cursor = self.conn.cursor()

        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
        }



    def delete_ip(self, ip):
        #从数据库中删除无效的ip
        delete_sql = f'''
            DELETE FROM ip_pool WHERE ip = "{ip}"
        '''
        self.cursor.execute(delete_sql)
        self.conn.commit()
        # res = self.cursor.fetchall()
        print("已删除")


    def judge_ip(self, ip, port):
        #判断一个ip是否可用
        proxy = {
            "http": f"http://{ip}:{port}",
            "https": f"http://{ip}:{port}"
        }
        url = "https://www.baidu.com/"
        try:
            response = requests.get(url=url,headers=self.headers, proxies=proxy, timeout=2)
            code = response.status_code
            # print("状态码类型：", type(code))
            if int(code) >= 200 and code < 300:
                print(f"代理ip：{ip}可用")
                print("准备插入到新的表中")
                #把当前可用的ip和端口保存到表ip_new中
                self.save_new_table(ip, port)
                return True
            else:
                print(f"获取的状态码为：{code}, 不可用即将删除")
                self.delete_ip(ip)
                return False
        except Exception as e:
            print(f"代理ip：{ip}异常，即将删除")
            self.delete_ip(ip)
            return False

    def get_random_ip(self):
        #从数据库中获取ip地址
        sql = '''
            SELECT ip,port FROM ip_pool ORDER BY RAND() LIMIT 1
        '''
        self.cursor.execute(sql)
        res = self.cursor.fetchall()[0]
        # print(res)
        ip, port = res[0], res[1]
        judge_res = self.judge_ip(ip, port)
        if judge_res:
            return f"http://{ip}:{port}"
        else:
            return self.get_random_ip()

    def save_new_table(self,ip, port):
        self.cursor.execute(
            f"insert into ip_new(ip,port) VALUES('{ip}' ,'{port}')"
        )
        self.conn.commit()
        print("成功插入到新的表中")


if __name__ == '__main__':
    get_ip = GetIP()
    for i in range(10):
        get_ip.get_random_ip()