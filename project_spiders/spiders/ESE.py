# -*- coding: utf-8 -*-
import scrapy
from project_spiders.items import ProjectSpidersItem
import project_spiders.spiders.Time_unite as Tu


class MathSpider(scrapy.Spider):
    name = 'ESE'
    allowed_domains = ['sustc.edu.cn']
    url = 'http://ese.sustc.edu.cn/research/lectures.aspx?page='
    offset = 1
    MAX_PAGE = 25

    start_urls = [
        url + str(offset)
    ]

    def parse(self, response):
        for each in response.xpath('//ul[@class="lec-ul"]/li'):
            item = ProjectSpidersItem()
            item['name'] = each.xpath("./a/div/p[1]/text()").extract()[0].strip()
            item['url'] = response.urljoin(each.xpath("./a/@href").extract()[0])
            item['department'] = self.name
            item['speaker'] = each.xpath("./a/div/p[2]/span[1]/text()").extract()[0].replace('演讲者：', '')
            item['place'] = each.xpath("./a/div/p[2]/span[3]/text()").extract()[0].replace('地点：', '')
            item['stime'] = Tu.ese(each.xpath("./a/div/p[2]/span[2]/text()").extract()[0].replace('时间：', ''))
            yield item
        if self.offset < self.MAX_PAGE:
            self.offset += 1
            yield scrapy.Request(self.url + str(self.offset), callback=self.parse)
