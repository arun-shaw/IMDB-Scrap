# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pyodbc

class ImdbcrawlPipeline(object):
    def __init__(self):
        self.create_Conn()


    def create_Conn(self):
        self.conn = pyodbc.connect('DRIVER={MySQL ODBC 8.0 ANSI Driver};SERVER=localhost;DATABASE=imdb_movies;UID=root;PWD=Welc0me@run')
        self.curr = self.conn.cursor()

    def store_db(self,item):
        self.curr.execute("""insert into World_Movies values (?,?,?,?,?,?,?)""",(
            item['Title'],
            item['Year'],
            item['Country_Code'],
            item['Genre'],
            item['Rating'],
            item['Plot'],
            item['Country_Name']

        ))
        self.conn.commit()

    def process_item(self, item, spider):
        self.store_db(item)
        return item
