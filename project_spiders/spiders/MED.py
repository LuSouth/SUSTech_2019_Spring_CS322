# -*- coding: utf-8 -*-
import scrapy
from project_spiders.items import ProjectSpidersItem
import project_spiders.spiders.Time_unite as Tu


class MathSpider(scrapy.Spider):
    name = 'MED'
    allowed_domains = ['sustech.edu.cn']
    url = 'http://med.sustech.edu.cn/lecture/id-136.html?page='
    offset = 1

    start_urls = [
        url + str(offset)
    ]

    def parse(self, response):
        for each in response.xpath('//li[@class="data-item "]'):
            item = ProjectSpidersItem()
            item['name'] = each.xpath("./a/span[2]/span[2]/span[1]/span/text()") \
                .extract()[0].strip().replace('Lecture：', '')
            item['url'] = response.urljoin(each.xpath("./a/@href").extract()[0])
            item['department'] = self.name
            item['speaker'] = each.xpath("./a/span[2]/span[2]/span[2]/span[1]/text()") \
                .extract()[0].replace('Speaker：', '')
            try:
                item['place'] = each.xpath("./a/span[2]/span[2]/span[2]/span[3]/text()") \
                    .extract()[0].replace('Location：', '')
            except IndexError:
                item['place'] = 'None'
            item['stime'] = Tu.med(each.xpath("./a/span[2]/span[2]/span[2]/span[2]/text()")
                                   .extract()[0].replace('Time：', ''))
            yield item
        if len(response.xpath('//li[@class="data-item "]')) > 0:
            self.offset += 1
            yield scrapy.Request(self.url + str(self.offset), callback=self.parse)
