# -*- coding: utf-8 -*-
import scrapy
from project_spiders.items import ProjectSpidersItem
import project_spiders.spiders.Time_unite as Tu


class MathSpider(scrapy.Spider):
    name = 'Math'
    allowed_domains = ['sustech.edu.cn']
    url = 'http://math.sustech.edu.cn/hall.html?lang=zh&page='
    offset = 1
    MAX_PAGE = 16

    start_urls = [
        url + str(offset)
    ]

    def parse(self, response):
        for each in response.xpath('//div[@class="newsAcademicListRow"]'):
            item = ProjectSpidersItem()
            item['name'] = each.xpath("./p[1]/a/text()").extract()[0]
            item['url'] = response.urljoin(each.xpath("./p[1]/a/@href").extract()[0])
            item['department'] = self.name
            try:
                index = 2
                item['speaker'] = item['place'] = item['stime'] = 'None'
                while True:
                    text = each.xpath("./p[" + str(index) + "]/text()").extract()[0]
                    if text.find('演讲者') > -1:
                        item['speaker'] = text.replace('演讲者：', '')
                    if text.find('地点') > -1:
                        item['place'] = text.replace('地点：', '')
                    if text.find('时间') > -1:
                        item['stime'] = Tu.unite(text.replace('时间：', ''))
                    index += 1
            except IndexError:
                pass
            yield item
        if self.offset < self.MAX_PAGE:
            self.offset += 1
            yield scrapy.Request(self.url + str(self.offset), callback=self.parse)
