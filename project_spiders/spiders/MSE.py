# -*- coding: utf-8 -*-
import scrapy
from project_spiders.items import ProjectSpidersItem
import project_spiders.spiders.Time_unite as Tu


class MseSpider(scrapy.Spider):
    name = 'MSE'
    allowed_domains = ['sustc.edu.cn']
    url = 'http://mse.sustc.edu.cn/cn/lecture/index/page/'
    offset = 1
    MAX_PAGE = 32
    start_urls = [
        url + str(offset)
    ]

    def parse(self, response):
        for each in response.xpath('//div[@class="section"]'):
            item = ProjectSpidersItem()
            item['name'] = each.xpath("./dl/dt/a/text()").extract()[0].replace('\r\n', '').strip(' ')
            item['url'] = response.urljoin(each.xpath("./dl/dt/a/@href").extract()[0])
            item['department'] = self.name
            text_list = each.xpath("./div/text()").extract()
            if len(text_list) > 0:
                item['stime'] = Tu.unite(text_list[0])
            else:
                item['stime'] = 'None'
            text_list = each.xpath("./dl/dd[1]/text()").extract()
            if len(text_list) > 0:
                item['speaker'] = text_list[0]
            else:
                item['speaker'] = 'None'
            text_list = each.xpath("./dl/dd[3]/text()").extract()
            if len(text_list) > 0:
                item['place'] = text_list[0]
            else:
                item['place'] = 'None'
            yield item
        if self.offset < self.MAX_PAGE:
            self.offset += 1
            yield scrapy.Request(self.url + str(self.offset), callback=self.parse)
