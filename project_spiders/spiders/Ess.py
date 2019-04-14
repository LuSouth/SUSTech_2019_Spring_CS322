# -*- coding: utf-8 -*-
import scrapy
from project_spiders.items import ProjectSpidersItem
import project_spiders.spiders.Time_unite as Tu


class EssSpider(scrapy.Spider):
    name = 'Ess'
    allowed_domains = ['sustech.edu.cn']
    url = 'http://ess.sustech.edu.cn/New-index-id-8-p-'
    offset = 1
    MAX_PAGE = 18

    start_urls = [
        url + str(offset) + '.html'
    ]

    def parse(self, response):
        for each in response.xpath('/html/body/div[3]/div[2]/div[2]/div/ul/li'):
            item = ProjectSpidersItem()
            item['name'] = each.xpath("./div[2]/h3/a/text()").extract()[0]
            item['url'] = response.urljoin(each.xpath("./div[2]/h3/a/@href").extract()[0])
            item['department'] = 'ESS'
            detail = each.xpath("./div[2]/p/text()").extract()[0]
            if detail.find("演讲者") > -1:
                item['speaker'] = detail[detail.find("演讲者") + 4:]
            else:
                item['speaker'] = 'None'
            if detail.find("时间") > -1:
                stime = None
                if detail.find("日", 0, 15) > -1:
                    stime = detail[detail.find("时间") + 3:detail.find("日")+1]
                if detail.find("号", 0, 15) > -1:
                    stime = detail[detail.find("时间") + 3:detail.find("号")+1]
                item['stime'] = Tu.ess(stime)
            else:
                item['stime'] = 'None'
            if detail.find("地点") > -1:
                item['place'] = detail[detail.find("地点") + 3:detail.find("演讲者") - 3]
            else:
                item['place'] = 'None'
            yield item
        if self.offset < self.MAX_PAGE:
            self.offset += 1
        yield scrapy.Request(self.url + str(self.offset) + '.html', callback=self.parse)
