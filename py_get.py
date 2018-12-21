import pdb

import scrapy


import mysql.connector
from sqlalchemy import create_engine
import sqlalchemy
import os
import threading


with open("dbline.txt",'r') as f:
    dbline = f.read().strip()

class Hander(object):
    engine = create_engine('mysql+mysqlconnector://%s@127.0.0.1:3306/trnet'%dbline)
    lock = threading.Lock()

    def insert(self, id,content,sub):
        # table = self._get_table_in_month(id_)
        #         self.lock.acquire()
#         with self.lock:
        with self.engine.connect() as con:
            cmd = """INSERT INTO company_test (id, content, sub) VALUES ({},\'{}\',\'{}\')""".format(id,content,sub)
            # print(cmd)
            result = con.execute(cmd)
                # print(result)
                # line = result.first()
        #             self.lock.release()
        # return line

# with open('ends.txt','r') as f:
#     line = f.readlines()
# line = [l.strip().split(':') for l in line]
# gets = {l[0]:int(l[1]) for l in line}

# pdb.set_trace()
pre  = 	[("B","25"),("C","25"),("D","25"),("E","25"),]
# pres = [ for a,b in pre]
start_urls = []
for a,b in pre:
    for i in range(int(b)):
        _ = 'http://shop.99114.com/list/pinyin/{}_{}'.format(a,i)
        start_urls.append(_)
    # start_urls = start_urls+[ for a,b in pre]
print("len start urls",len(start_urls))


class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = start_urls
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, sdch",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Host": "www.xxxxxx.com",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) "+
                      "AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"
    }
    head = Hander()

    def parse(self, response):
        # re =//*[@id="footerTop"]/ul/li[1]/a[2]
        for re in response.xpath('//*[@id="footerTop"]/ul/li/a'):
            sub = re.xpath('@href').extract_first()
            content = re.xpath('b/text()').extract_first()
            id = sub.split('/')[-1]
#             print(id,sub,content)

            try:
                self.head.insert(id,content,sub)
            except mysql.connector.errors.IntegrityError as e:
                print(e)
                pass
            except sqlalchemy.exc.IntegrityError as e:
                print(e)
                pass
            # except sqlalchemy.exc
            # except sqlalchemy.exc
            except mysql.connector.errors.ProgrammingError as e:
                if content.find(','):
                    content = content.replace('\'', '')
                    self.head.insert(id, content, sub)
                pdb.set_trace()
            # pdb.set_trace()
        # for title in response.css('.post-header>h2'):
        #     yield {'title': title.css('a ::text').extract_first()}