# -*- coding: utf-8 -*-
import scrapy
from project_spiders.items import ProjectSpidersItem
import project_spiders.spiders.Time_unite as Tu


class ChemistrySpider(scrapy.Spider):
    name = 'Chemistry'
    allowed_domains = ['sustc.edu.cn']
    url = 'http://chem.sustc.edu.cn/index.php/dynamic/index/p/'
    offset = 1
    MAX_PAGE = 8
    start_urls = [
        url + str(offset) + '.html'
    ]

    def parse(self, response):
        div_list = response.xpath('//div[@class="ch_content_dynamic"]/div')
        div_list.pop(0)
        for each in div_list:
            item = ProjectSpidersItem()
            item['name'] = each.xpath("./a/div[2]/div[1]/text()").extract()[0]
            item['url'] = response.urljoin(each.xpath("./a/@href").extract()[0])
            item['department'] = 'Chemistry'
            text_list = each.xpath("./a/div[2]/p/span/text()").extract()
            if len(text_list) > 0:
                item['stime'] = Tu.unite(text_list[0])
            else:
                item['stime'] = 'None'
            text_list = each.xpath("./a/div[2]/div[2]/div/span[1]/text()").extract()
            if len(text_list) > 0:
                item['speaker'] = text_list[0]
            else:
                item['speaker'] = 'None'
            text_list = each.xpath("./a/div[2]/div[2]/div/span[3]/text()").extract()
            if len(text_list) > 0:
                item['place'] = text_list[0]
            else:
                item['place'] = 'None'
            yield item
        if self.offset < self.MAX_PAGE:
            self.offset += 1
        yield scrapy.Request(self.url + str(self.offset) + '.html', callback=self.parse)
