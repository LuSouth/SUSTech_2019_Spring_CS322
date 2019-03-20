# -*- coding: utf-8 -*-
import re
import os
import time
import requests
import Headers


class MSE:
    def __init__(self):
        self.url = 'http://mse.sustc.edu.cn/cn/lecture/index/page/'
        self.title = 'http://mse.sustc.edu.cn'
        self.page = 1
        self.max_page = 31
        if not os.path.exists('MSE'):
            os.makedirs('MSE')
        self.error_file = open('MSE/Error_message' + '.txt', "w", encoding='utf-8')

    def matching(self, text, file):
        name_pattern = re.compile(r'title=".*?"')
        url_pattern = re.compile(r'<a href=".*?"')
        detail_pattern = re.compile(r'<dd>.*?</dd>')
        time_pattern = re.compile(r'<div class="time".*?</div>')
        speaker = 'None'
        place = 'None'
        stime = re.search(time_pattern, text).group()
        stime = Headers.delect_bracket(stime)
        try:
            name = re.search(name_pattern, text).group()[7:-1]
        except AttributeError:
            self.error_file.write('Error at matching: Name is none\n')
            return
        try:
            url = re.search(url_pattern, text).group()[9:-1]
            url = self.title + url
        except AttributeError:
            self.error_file.write('Error at matching: URL is none\n')
            return
        m = re.findall(detail_pattern, text)
        for item in m:
            item = Headers.delect_bracket(item)
            if item.find('演讲者') > -1:
                speaker = item.replace('演讲者：', '')
            else:
                if item.find('地点') > -1:
                    place = item.replace('地点：', '')
                else:
                    if item.find('时间') > -1:
                        stime += ' ' + item.replace('时间：', '')
        file.write(name + '\n')
        file.write(url + '\n')
        file.write(speaker + '\n')
        file.write(stime + '\n')
        file.write(place + '\n\n')

    def recognition(self, text, file):
        div_pattern = re.compile(r'<div class="section".*?</a>.*?</div>', re.DOTALL)
        try:
            m = re.findall(div_pattern, text)
            num = 0
            for item in m:
                num += 1
                self.error_file.write('Matching Page' + str(self.page) + ' NO.' + str(num) + '\n')
                self.matching(item, file)
        except AttributeError as e:
            self.error_file.write('Error at ' + str(self.page) + ' recognition\n' + str(e.args))

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
            file = open('MSE/Page' + str(self.page) + '.txt', "w", encoding='utf-8')
            self.recognition(html.text, file)
            file.close()
            self.page += 1
        self.error_file.write(time.strftime("%b %d %Y %H:%M:%S", time.localtime()))
        self.error_file.close()


if __name__ == '__main__':
    a = MSE()
    a.start()
