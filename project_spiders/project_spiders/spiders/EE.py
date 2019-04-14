# -*- coding: utf-8 -*-
import scrapy
from project_spiders.items import ProjectSpidersItem
import requests
import re
import project_spiders.spiders.Time_unite as Tu


class EeSpider(scrapy.Spider):
    name = 'EE'
    allowed_domains = ['sustc.edu.cn']
    url = 'https://eee.sustc.edu.cn/?cat=7&cc=7&paged='
    offset = 1
    MAX_PAGE = 67
    start_urls = [
        url + str(offset)
    ]

    def parse(self, response):
        for each in response.xpath('//li[@id="xwdt1_li1"]'):
            item = ProjectSpidersItem()
            item['name'] = each.xpath("./a/div[2]/h5/text()").extract()[0].replace('\r\n', '').strip(' ')
            item['url'] = response.urljoin(each.xpath("./a/@href").extract()[0])
            item['department'] = 'EE'
            item['speaker'] = item['stime'] = item['place'] = 'None'
            detail_list = each.xpath("./a/div[2]/div")
            for detail in detail_list:
                text = detail.xpath("./text()").extract()
                if len(text) > 0:
                    if '演讲' in text[0]:
                        item['speaker'] = text[0][4:]
                    if '地点' in text[0]:
                        item['place'] = text[0][3:]
            detail_list = each.xpath("./a/div[2]/p")
            for detail in detail_list:
                text = detail.xpath("./text()").extract()
                if len(text) == 1:
                    if '演讲' in text[0]:
                        item['speaker'] = text[0][4:]
                    if '地点' in text[0]:
                        item['place'] = text[0][3:]
                if len(text) > 1:
                    for d_text in text:
                        if '演讲' in d_text:
                            item['speaker'] = d_text.strip()[4:]
                        if '地点' in d_text:
                            item['place'] = d_text.strip()[3:]
            detail_list = each.xpath("./a/div[2]/div[1]/p")
            for detail in detail_list:
                text = detail.xpath("./text()").extract()
                if len(text) > 0:
                    if '演讲' in text[0]:
                        item['speaker'] = text[0][4:]
                    if '地点' in text[0]:
                        item['place'] = text[0][3:]
            item['stime'] = Tu.unite(self.get_clear_time(item['url']))
            yield item
        if self.offset < self.MAX_PAGE:
            self.offset += 1
        yield scrapy.Request(self.url + str(self.offset), callback=self.parse)

    def get_clear_time(self, url):
        html = requests.get(url, timeout=5)
        time_pattern = re.compile(r'<span> 日期.*?</span>')
        stime = re.search(time_pattern, html.text).group()
        return stime[9:-7]
