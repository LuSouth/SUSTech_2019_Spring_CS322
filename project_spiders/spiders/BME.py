# -*- coding: utf-8 -*-
import scrapy
from project_spiders.items import ProjectSpidersItem
import project_spiders.spiders.Time_unite as Tu


class MathSpider(scrapy.Spider):
    name = 'BME'
    allowed_domains = ['sustech.edu.cn']
    url = 'http://bme.sustech.edu.cn/category/news/lecture/page/'
    offset = 1
    MAX_PAGE = 13

    start_urls = [
        url + str(offset)
    ]

    def parse(self, response):
        for each in response.xpath('//div[@class="ny_tzgg clearfix"]/div'):
            item = ProjectSpidersItem()
            item['name'] = each.xpath("./a/div[2]/h3/text()").extract()[0].strip()
            item['url'] = response.urljoin(each.xpath("./a/@href").extract()[0])
            item['department'] = self.name
            year = each.xpath("./a/div[1]/div[2]/text()").extract()[1]
            item['stime'] = Tu.bme(each.xpath('./a/div[2]/p[1]/text()').extract()[0], year)
            item['place'] = each.xpath('./a/div[2]/p[2]/text()').extract()[0]
            try:
                item['speaker'] = each.xpath('./a/div[2]/p[3]/span/text()').extract()[0]
            except IndexError:
                if item['name'].find('：') != -1:
                    item['speaker'] = item['name'].split('：')[0]
                else:
                    if item['name'].find(':') != -1:
                        item['speaker'] = item['name'].split(':')[0]
                    else:
                        item['speaker'] = 'None'
            yield item
        if self.offset < self.MAX_PAGE:
            self.offset += 1
            yield scrapy.Request(self.url + str(self.offset), callback=self.parse)
