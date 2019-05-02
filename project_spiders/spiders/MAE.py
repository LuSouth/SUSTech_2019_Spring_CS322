# -*- coding: utf-8 -*-
import scrapy
from project_spiders.items import ProjectSpidersItem
import project_spiders.spiders.Time_unite as Tu


class MathSpider(scrapy.Spider):
    name = 'MAE'
    allowed_domains = ['sustech.edu.cn']

    start_urls = [
        'http://mae.sustech.edu.cn/cn/notice/jiangzuo/index.html',
        'http://mae.sustech.edu.cn/cn/notice/jiangzuo/2.html'
    ]

    def parse(self, response):
        for each in response.xpath('//ul[@class="info-list"]/li'):
            item = ProjectSpidersItem()
            item['name'] = each.xpath("./div/h4/a/text()").extract()[0].strip()
            item['url'] = response.urljoin(each.xpath("./div/h4/a/@href").extract()[0])
            item['department'] = self.name
            item['speaker'] = each.xpath("./div/div/ul/li[1]/span/text()").extract()[0].replace('演讲者：', '')
            try:
                item['place'] = each.xpath("./div/div/ul/li[3]/span/text()").extract()[0].replace('地点：', '')
            except IndexError:
                item['place'] = 'None'
            item['stime'] = Tu.unite(each.xpath("./div/div/ul/li[2]/span/text()").extract()[0].replace('时间：', ''))
            yield item
