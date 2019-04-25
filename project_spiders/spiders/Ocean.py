# -*- coding: utf-8 -*-
import scrapy
from project_spiders.items import ProjectSpidersItem
import project_spiders.spiders.Time_unite as Tu
import json


class MathSpider(scrapy.Spider):
    name = 'Ocean'
    allowed_domains = ['sustech.edu.cn']
    url = 'https://ocean.sustech.edu.cn/ocean/public/api/lecture/getLectureList?cid=43&page='
    offset = 1
    MAX_PAGE = 17  # 初始最大页面数，会根据返回数据更改

    start_urls = [
        url + str(offset) + '&limit=4&language=cn'
    ]

    def parse(self, response):
        rs = json.loads(response.body)
        item = ProjectSpidersItem()
        self.MAX_PAGE = rs['totle']
        for value in rs['data']:
            item['name'] = value['lecture_title']
            item['department'] = self.name
            item['speaker'] = value['lecture_speaker']
            item['stime'] = Tu.unite(value['lecture_addtime'])
            item['place'] = value['lecture_address']
            item['url'] = response.urljoin('/views/details_lecture.html?id=' + str(value['id']))
            yield item
        if self.offset < self.MAX_PAGE:
            self.offset += 1
            yield scrapy.Request(self.url + str(self.offset) + '&limit=4&language=cn', callback=self.parse)
