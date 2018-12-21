# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import mysql.connector
from sqlalchemy import create_engine
import sqlalchemy


with open("dbline.txt",'r') as f:
    MYSQL_HANDER = f.read().strip()


# class PyGetPipeline(object):
#
#     def open_spider(self, spider):
#         self.engine = create_engine(MYSQL_HANDER)
#
#     def process_item(self, item, spider):
#         id, content, sub = item['data']['id'],item['data']['content'],item['data']['sub']
#         with self.engine.connect() as con:
#             cmd = """INSERT INTO company_test (id, content, sub) VALUES ({},\'{}\',\'{}\')""".format(id,content,sub)
#             # print(cmd)
#             result = con.execute(cmd)
#
#         return item

from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import String, Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Company(Base):
    __tablename__ = "company_test"
    id = Column(Integer, primary_key=True)
    content = Column(String(127))
    sub = Column(String(255))

class PyGetManyPipeline(object):

    def open_spider(self, spider):
        # self.engine = create_engine('mysql+mysqlconnector://%s@127.0.0.1:3306/trnet'%dbline)
        engine = create_engine(MYSQL_HANDER)

        self.session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.session()
        for data in item['data']:
            id, content, sub = int(data['id']),data['content'],data['sub']
            line = Company(id=id,content=content,sub=sub)
            session.add(line)
        session.commit()
        # with self.engine.connect() as con:
        #     cmd = """INSERT INTO company_test (id, content, sub) VALUES ({},\'{}\',\'{}\')""".format(id,content,sub)
            # print(cmd)
            # result = con.execute(cmd)

        return item
