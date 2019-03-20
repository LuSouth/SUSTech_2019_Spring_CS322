# -*- coding: utf-8 -*-
import re
import os
import time
import requests
import Headers


class Chemistry:
    def __init__(self):
        self.url = 'http://chem.sustc.edu.cn/index.php/dynamic/index/p/'
        self.title = 'http://chem.sustc.edu.cn'
        self.page = 1
        self.max_page = 9
        if not os.path.exists('Chemistry'):
            os.makedirs('Chemistry')
        self.error_file = open('Chemistry/Error_message' + '.txt', "w", encoding='utf-8')

    def matching(self, text, file):
        name_pattern = re.compile(r'<div class="ch_dynamic_title" style="">.*?</div>')
        url_pattern = re.compile(r'<a href=.*?">')
        stime_pattern = re.compile(r'<p class="ch_news_r_date "><span class="ch_dynamic_date">.*?</span>')
        speaker_pattern = re.compile(r'演讲者：</span>.*?</span>')
        speaker = 'None'
        place = 'None'
        stime = 'None'
        try:
            name = re.search(name_pattern, text).group()[39:-6]
        except AttributeError:
            self.error_file.write('Error at matching: Name is none\n')
            return
        try:
            url = re.search(url_pattern, text).group()[9:-2]
            url = self.title + url
        except AttributeError:
            self.error_file.write('Error at matching: URL is none\n')
            return
        try:
            speaker = re.search(speaker_pattern, text).group()[11:-7].replace('&nbsp;', '')
        except AttributeError:
            self.error_file.write('Error at matching: speaker lost\n')
            return
        try:
            stime = re.search(stime_pattern, text).group()[57:-7].replace('&nbsp;', '')
        except AttributeError:
            self.error_file.write('Error at matching: time lost\n')
            return
        file.write(name + '\n')
        file.write(url + '\n')
        file.write(speaker + '\n')
        file.write(stime + '\n')
        file.write(place + '\n\n')

    def recognition(self, text, file):
        div_pattern = re.compile(r'<div class="ch_dynamic_contents.*?</a>.*?</div>', re.DOTALL)
        try:
            m = re.findall(div_pattern, text)
            num = 0
            for item in m:
                num += 1
                self.error_file.write('Matching Page' + str(self.page) + ' NO.' + str(num) + '\n')
                self.matching(item, file)
                file.write('\n')
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
            file = open('Chemistry/Page' + str(self.page) + '.txt', "w", encoding='utf-8')
            self.recognition(html.text, file)
            file.close()
            self.page += 1
        self.error_file.write(time.strftime("%b %d %Y %H:%M:%S", time.localtime()))
        self.error_file.close()


if __name__ == '__main__':
    a = Chemistry()
    a.start()
