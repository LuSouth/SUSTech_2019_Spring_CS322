# -*- coding: utf-8 -*-
import scrapy
from project_spiders.items import ProjectSpidersItem
import project_spiders.spiders.Time_unite as Tu


class MathSpider(scrapy.Spider):
    name = 'MEE'
    allowed_domains = ['sustech.edu.cn']
    url = 'http://mee.sustech.edu.cn/cn/abouts/seminar/'
    offset = 1
    MAX_PAGE = 21

    start_urls = [
        'http://mee.sustech.edu.cn/cn/abouts/seminar/index.html'
    ]

    def parse(self, response):
        for each in response.xpath('//ul[@class="info-list"]/li'):
            item = ProjectSpidersItem()
            item['name'] = each.xpath("./a/text()").extract()[0].strip()
            item['url'] = response.urljoin(each.xpath("./a/@href").extract()[0])
            item['department'] = self.name
            item['stime'] = 'None'
            item['speaker'] = 'None'
            item['place'] = 'None'
            for detail in each.xpath('./div/ul/li'):
                if detail.xpath('./strong/text()').extract()[0].find('时间') != -1:
                    item['stime'] = Tu.unite(detail.xpath('./span/text()').extract()[0])
                if detail.xpath('./strong/text()').extract()[0].find('地点') != -1:
                    item['place'] = detail.xpath('./span/text()').extract()[0]
                if detail.xpath('./strong/text()').extract()[0].find('演讲') != -1:
                    item['speaker'] = detail.xpath('./span/text()').extract()[0]
            yield item
        if self.offset < self.MAX_PAGE:
            self.offset += 1
            yield scrapy.Request(self.url + str(self.offset) + '.html', callback=self.parse)
