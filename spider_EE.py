# -*- coding: utf-8 -*-
import re
import os
import time
import requests
import Headers


class EE:
    def __init__(self):
        self.url = 'https://eee.sustc.edu.cn/?cat=7&cc=7&paged='
        self.title = 'http://eee.sustc.edu.cn'
        self.page = 1
        self.max_page = 67
        self.department = 'EE'
        if not os.path.exists(self.department):
            os.makedirs(self.department)
        self.error_file = open(self.department + '/Error_message' + '.txt', "w", encoding='utf-8')
        self.file_all = open(self.department+ '/' + self.department + '_all.csv', "w", encoding='utf-8')

    def get_clear_time(self, url):
        header = Headers.get_header()
        html = requests.get(url, header, timeout=5)
        time_pattern = re.compile(r'<span> 日期.*?</span>')
        stime = re.search(time_pattern, html.text).group()
        return stime[9:-7]

    def matching(self, text, file):
        name_pattern = re.compile(r'<h5>.*?</h5>')
        url_pattern = re.compile(r'<a href=.*?">')
        detail_pattern = re.compile(r'<p>.*?</p>', re.DOTALL)
        speaker = 'None'
        place = 'None'
        stime = 'None'
        try:
            name = re.search(name_pattern, text).group()[4:-5]
        except AttributeError:
            self.error_file.write('Error at matching: Name is none\n')
            return
        try:
            url = re.search(url_pattern, text).group()[9:-2]
        except AttributeError:
            self.error_file.write('Error at matching: URL is none\n')
            return
        m = re.findall(detail_pattern, text)
        for item in m:
            if item.find('地点') > -1 and item.find('时间') > -1:
                if item.find('演讲') > -1:
                    speaker = item[item.find('演讲')+4:item.find('时间')]
                if item.find('20-21 Oct') >= 0:
                    stime = '10月20日'
                else:
                    stime = item[item.find('时间')+3:item.find('月')+2]
                place = item[item.find('地点')+3:]
                continue
            item = Headers.delect_bracket(item)
            if item.find('演讲') > -1:
                speaker = item[4:]
            else:
                if item.find('地点') > -1:
                    place = item.replace('地点：', '')
        stime = self.get_clear_time(url)
        content = '"' + name + '",' \
            '"' + url + '",' \
            '"' + speaker + '",' \
            '"' + stime + '",' \
            '"' + self.department + '",' \
            '"' + place + '",\n'
        file.write(content)
        self.file_all.write(content)

    def recognition(self, text, file):
        div_pattern = re.compile(r'<li id="xwdt1_li1">.*?</li>', re.DOTALL)
        try:
            m = re.findall(div_pattern, text)
            num = 0
            for item in m:
                num += 1
                self.error_file.write('Matching Page' + str(self.page) + ' NO.' + str(num) + '\n')
                self.matching(item, file)
        except AttributeError:
            self.error_file.write('Error at ' + str(self.page) + ' recognition\n')

    def start(self):
        header = Headers.get_header()
        while self.page <= self.max_page:
            url = self.url + str(self.page)
            try:
                html = requests.get(url, header, timeout=5)
                if html.text == '':
                    self.error_file.write('Can not get the web file!\n')
                    exit(0)
            except requests.exceptions.ConnectionError as e:
                self.error_file.write('Error At 0: ' + str(e.args) + '\n')
                return
            file = open(self.department + '/Page' + str(self.page) + '.txt', "w", encoding='utf-8')
            self.recognition(html.text, file)
            file.close()
            self.page += 1
        self.error_file.write(time.strftime("%b %d %Y %H:%M:%S", time.localtime()))
        self.error_file.close()
        self.file_all.close()


if __name__ == '__main__':
    a = EE()
    a.start()
