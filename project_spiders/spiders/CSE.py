# -*- coding: utf-8 -*-
import scrapy
from project_spiders.items import ProjectSpidersItem
import project_spiders.spiders.Time_unite as Tu


class MathSpider(scrapy.Spider):
    name = 'CSE'
    allowed_domains = ['sustech.edu.cn']
    url = 'http://cse.sustech.edu.cn/cn/lecture/index/page/'
    offset = 1
    MAX_PAGE = 21

    start_urls = [
        url + str(offset)
    ]

    def parse(self, response):
        try:
            self.MAX_PAGE = int(response.xpath('//li[@class="last"]/a/@href').extract()[0].split('/')[-1])
        except IndexError:
            pass
        for each in response.xpath('//div[@class="main"]'):
            item = ProjectSpidersItem()
            item['name'] = each.xpath("./dl/dt/a/text()").extract()[0]
            item['url'] = response.urljoin(each.xpath("./dl/dt/a/@href").extract()[0])
            item['department'] = self.name
            try:
                item['speaker'] = each.xpath("./dl/dd[@class='name']/text()").extract()[0].replace('演讲者：', '')
            except IndexError:
                item['speaker'] = 'None'
            try:
                item['place'] = each.xpath("./dl/dd[@class='place']/text()").extract()[0].replace('地点：', '')
            except IndexError:
                item['place'] = 'None'
            try:
                item['stime'] = Tu.unite(each.xpath("./dl/dd[@class='date']/text()").extract()[0].replace('时间：', ''))
            except IndexError:
                item['stime'] = 'None'
            yield item
        if self.offset < self.MAX_PAGE:
            self.offset += 1
            yield scrapy.Request(self.url + str(self.offset), callback=self.parse)
