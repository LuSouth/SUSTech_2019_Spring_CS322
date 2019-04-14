# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# import csv
import os


class ProjectSpidersPipeline(object):

    def __init__(self):
        self.filename = None

    def open_spider(self, spider):
        if os.path.exists(spider.name + ".csv"):
            if os.path.exists(spider.name + ".csv.bak"):
                os.remove(spider.name + ".csv.bak")
            os.rename(spider.name + ".csv", spider.name + ".csv.bak")
        self.filename = open(spider.name + ".csv", "w", encoding='utf-8')

    def process_item(self, item, spider):
        if item['speaker'] == '':
            item['speaker'] = 'None'
        if item['place'] == '':
            item['place'] = 'None'
        content = "'" + item['name'] + "'," \
            "'" + item['url'] + "'," \
            "'" + item['speaker'] + "'," \
            "'" + item['stime'] + "'," \
            "'" + item['department'] + "'," \
            "'" + item['place'] + "',\n"
        self.filename.write(content.encode().decode('utf-8'))
        # csv.writer(self.filename)\
        #     .writerow((item['name'], item['url'], item['stime'], item['department'], item['place']))
        return item

    def close_spider(self, spider):
        self.filename.close()
