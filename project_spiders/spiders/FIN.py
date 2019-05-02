# -*- coding: utf-8 -*-
import scrapy
from project_spiders.items import ProjectSpidersItem
import project_spiders.spiders.Time_unite as Tu


class MathSpider(scrapy.Spider):
    name = 'FIN'
    allowed_domains = ['sustech.edu.cn']

    start_urls = [
        'http://fin.sustech.edu.cn/news3.aspx?TypeId=126&FId=t2:126:2'
    ]

    def parse(self, response):
        for each in response.xpath('//div[@class="nnews3_lb3_m"]'):
            item = ProjectSpidersItem()
            item['name'] = each.xpath('./div[1]/text()').extract()[0].strip()
            item['url'] = 'http://fin.sustech.edu.cn/news3.aspx?TypeId=126&FId=t2:126:2'
            item['department'] = self.name
            try:
                item['speaker'] = each.xpath('./div[2]/div[1]/text()').extract()[1].strip()
                if item['speaker'] == '\\' or item['speaker'] == '':
                    continue
            except IndexError:
                continue
            try:
                item['place'] = each.xpath('./div[2]/div[3]/span[2]/text()').extract()[0].strip()
            except IndexError:
                item['place'] = 'None'
            item['stime'] = Tu.fin(each.xpath('./div[2]/div[2]/text()').extract()[1].strip())
            yield item
