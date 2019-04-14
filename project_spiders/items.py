# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProjectSpidersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 讲座名
    name = scrapy.Field()
    # 讲座链接
    url = scrapy.Field()
    # 演讲者
    speaker = scrapy.Field()
    # 演讲地点
    place = scrapy.Field()
    # 演讲时间
    stime = scrapy.Field()
    # 院系
    department = scrapy.Field()

