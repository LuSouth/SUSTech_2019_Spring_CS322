# -*- coding: utf-8 -*-
import re
import os
import time
import requests
import Headers


class Physics:
    def __init__(self):
        self.url = 'https://phy.sustc.edu.cn/index.php?s=/List/index/cid/33/p/'
        self.title = 'http://phy.sustc.edu.cn'
        self.page = 1
        self.max_page = 21
        if not os.path.exists('Physics'):
            os.makedirs('Physics')
        self.error_file = open('Physics/Error_message' + '.txt', "w", encoding='utf-8')

    def matching(self, text, file):
        name_pattern = re.compile(r'">.*?</a>')
        url_pattern = re.compile(r'<a href=.*?">')
        stime_pattern = re.compile(r'time">.*?</span>')
        detail_pattern = re.compile(r'<span>.*?</span>')
        speaker = 'None'
        place = 'None'
        try:
            name = re.search(name_pattern, text).group()[3:-4]
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
            stime = re.search(stime_pattern, text).group()[6:-7]
            stime = stime[:4]
        except AttributeError:
            self.error_file.write('Error at matching: Day is none\n')
            return
        m = re.findall(detail_pattern, text)
        for item in m:
            item = item[6:-7]
            if item.find('演讲者') == 0:
                speaker = item[4:]
            else:
                if item.find('地点') == 0:
                    place = item[3:]
                else:
                    if item.find('时间') == 0:
                        stime += ' ' + item[3:-1]
        file.write(name + '\n')
        file.write(url + '\n')
        file.write(speaker + '\n')
        file.write(stime + '\n')
        file.write(place + '\n\n')

    def recognition(self, text, file):
        ul_pattern = re.compile(r'<ul class="list-unstyled">.*?</ul>', re.DOTALL)
        div_pattern = re.compile(r'<div>.*?<span class="time">.*?</div>', re.DOTALL)
        ul = None
        try:
            ul = re.search(ul_pattern, text).group()
        except AttributeError:
            self.error_file.write('Error at ' + str(self.page) + ' ul\n')
        try:
            m = re.findall(div_pattern, ul)
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
            url = self.url + str(self.page) + '.html'
            try:
                html = requests.get(url, header, timeout=5)
                if html.text == '':
                    self.error_file.write('Can not get the web file!\n')
                    exit(0)
            except requests.exceptions.ConnectionError as e:
                self.error_file.write('Error At 0: ' + str(e.args) + '\n')
                return
            file = open('Physics/Page' + str(self.page) + '.txt', "w", encoding='utf-8')
            # file.write(html.text)
            self.recognition(html.text, file)
            file.close()
            self.page += 1
        self.error_file.write(time.strftime("%b %d %Y %H:%M:%S", time.localtime()))
        self.error_file.close()


if __name__ == '__main__':
    a = Physics()
    a.start()
