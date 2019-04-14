# -*- coding: utf-8 -*-
import scrapy
from project_spiders.items import ProjectSpidersItem
import project_spiders.spiders.Time_unite as Tu


class PhysicsSpider(scrapy.Spider):
    name = 'Physics'
    allowed_domains = ['sustc.edu.cn']
    url = 'https://phy.sustc.edu.cn/index.php?s=/List/index/cid/33/p/'
    offset = 1
    MAX_PAGE = 22

    start_urls = [
        url + str(offset) + '.html'
    ]

    def parse(self, response):
        for each in response.xpath('/html/body/div[5]/div/div/ul/li'):
            item = ProjectSpidersItem()
            item['department'] = 'Physics'
            item['name'] = each.xpath('./div/h4/a/text()').extract()[0]
            item['url'] = response.urljoin(each.xpath('./div/h4/a/@href').extract()[0])
            publish_year = each.xpath('./div/span/text()').extract()[0]
            publish_day = each.xpath('./div/span/text()').extract()[1].replace('/', '-')
            try:
                index = 1
                item['speaker'] = item['place'] = item['stime'] = 'None'
                while True:
                    text = each.xpath('./div/div/span[' + str(index) + ']/text()').extract()[0]
                    if text.find('演讲者') > -1:
                        item['speaker'] = text.replace('演讲者：', '')
                    if text.find('地点') > -1:
                        item['place'] = text.replace('地点：', '')
                    if text.find('时间') > -1:
                        item['stime'] = text.replace('时间：', '')
                        old_time = text.replace('时间：', '')
                        item['stime'] = Tu.physic(old_time, publish_year + '-' + publish_day)
                    index += 1
            except IndexError:
                pass
            yield item
        if self.offset < self.MAX_PAGE:
            self.offset += 1
        yield scrapy.Request(self.url + str(self.offset) + '.html', callback=self.parse)