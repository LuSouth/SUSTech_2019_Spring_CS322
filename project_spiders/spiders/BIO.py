# -*- coding: utf-8 -*-
import scrapy
from project_spiders.items import ProjectSpidersItem
import project_spiders.spiders.Time_unite as Tu


class MathSpider(scrapy.Spider):
    name = 'BIO'
    allowed_domains = ['sustc.edu.cn']
    url = 'https://bio.sustc.edu.cn/?cat=17&paged='
    offset = 1
    MAX_PAGE = 20
    re_year = 2019
    pas_month = 12

    start_urls = [
        url + str(offset)
    ]

    def parse(self, response):
        for each in response.xpath('//div[@class="div_conter"]'):
            item = ProjectSpidersItem()
            item['name'] = each.xpath("./p/a/@title").extract()[0].strip()
            item['url'] = response.urljoin(each.xpath("./p/a/@href").extract()[0])
            item['department'] = self.name
            detail = each.xpath("./div/div/p/text()").extract()
            if len(detail) == 1:
                detail = detail[0].strip().replace(' ', '').replace(' ', '').replace('\xa0', '')
                detail = detail.split('\n')
                for it in detail:
                    it = it.strip()
                    if it.find('时间') != -1:
                        if self.pas_month < int(it[3:it.find('月')]):
                            self.re_year -= 1
                        item['stime'] = Tu.bio(it[3:].strip(), self.re_year)
                        self.pas_month = int(item['stime'].split('-')[1])
                    if it.find('地点') != -1:
                        item['place'] = it[3:].strip()
                    if it.find('报告') != -1:
                        item['speaker'] = it[4:].strip()
            if len(detail) > 1:
                item['speaker'] = 'None'
                item['place'] = 'None'
                item['stime'] = 'None'
                for it in detail:
                    it = it.strip().replace(' ', '').replace(' ', '').replace('\xa0', '')
                    if it.find('年') != -1:
                        continue
                    if it.find('时间') != -1:
                        if it.find('月') != -1:
                            if self.pas_month < int(it[3:it.find('月')]):
                                self.re_year -= 1
                            item['stime'] = Tu.bio(it[3:].strip(), self.re_year)
                            self.pas_month = int(item['stime'].split('-')[1])
                    if it.find('地点') != -1:
                        item['place'] = it[3:].strip()
                    if it.find('报告') != -1:
                        item['speaker'] = it[4:].strip()
                    if it.find('演讲') != -1:
                        item['speaker'] = it[4:].strip()
            yield item
        if self.offset < self.MAX_PAGE:
            self.offset += 1
            yield scrapy.Request(self.url + str(self.offset), callback=self.parse)
