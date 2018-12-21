import pdb

import scrapy


import mysql.connector
from sqlalchemy import create_engine
import sqlalchemy
import os
from py_get.items import PyGetItem

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
    name = 'company'
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
    # head = Hander()

#     def parse_one(self, response):
#         # re =//*[@id="footerTop"]/ul/li[1]/a[2]
#
#         for re in response.xpath('//*[@id="footerTop"]/ul/li/a'):
#             sub = re.xpath('@href').extract_first()
#             content = re.xpath('b/text()').extract_first()
#             id = sub.split('/')[-1]
# #             print(id,sub,content)
#             item = PyGetItem()
#
#             item['data'] = {
#                 'id':id,
#                 'sub':sub,
#                 'content':content,
#             }
#             yield item

    def parse(self, response):
        # re =//*[@id="footerTop"]/ul/li[1]/a[2]
        item = PyGetItem()
        item['data'] = []

        for re in response.xpath('//*[@id="footerTop"]/ul/li/a'):
            sub = re.xpath('@href').extract_first()
            content = re.xpath('b/text()').extract_first()
            id = sub.split('/')[-1]
            #             print(id,sub,content)
            _ = {
                'id': id,
                'sub': sub,
                'content': content,
            }
            item['data'].append(_)
        # return item
            # try:
            #     self.head.insert(id,content,sub)
            # except mysql.connector.errors.IntegrityError as e:
            #     print(e)
            #     pass
            # except sqlalchemy.exc.IntegrityError as e:
            #     print(e)
            #     pass
            # # except sqlalchemy.exc
            # # except sqlalchemy.exc
            # except mysql.connector.errors.ProgrammingError as e:
            #     if content.find(','):
            #         content = content.replace('\'', '')
            #         self.head.insert(id, content, sub)
            #     pdb.set_trace()