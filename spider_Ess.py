# -*- coding: utf-8 -*-
import re
import os
import time
import requests
import Headers


class Ess:
    def __init__(self):
        self.url = 'http://ess.sustc.edu.cn/New-index-id-8-p-'
        self.title = 'http://ess.sustc.edu.cn'
        self.page = 1
        self.max_page = 16
        if not os.path.exists('Ess'):
            os.makedirs('Ess')
        self.error_file = open('Ess/Error_message' + '.txt', "w", encoding='utf-8')

    def matching(self, text, file):
        name_pattern = re.compile(r'">.*?</a>')
        url_pattern = re.compile(r'<a href=.*?">')
        detail_pattern = re.compile(r'<p.*?</p>')
        speaker = 'None'
        place = 'None'
        stime = 'None'
        try:
            name = re.search(name_pattern, text).group()[2:-4]
            name = name[name.find('<')+1:]
        except AttributeError:
            self.error_file.write('Error at matching: Name is none\n')
            return
        try:
            url = re.search(url_pattern, text).group()[9:-2]
            url = self.title + url
        except AttributeError:
            self.error_file.write('Error at matching: URL is none\n')
            return
        m = re.findall(detail_pattern, text)
        for item in m:
            item = item[item.find('>'):-4]
            if item.find("演讲者") > -1:
                speaker = item[item.find("演讲者")+4:]
            if item.find("时间") > -1:
                stime = item[item.find("时间")+3:item.find("地点")-3]
            if item.find("地点") > -1:
                place = item[item.find("地点")+3:item.find("演讲者")-3]
        file.write(name + '\n')
        file.write(url + '\n')
        file.write(speaker + '\n')
        file.write(stime + '\n')
        file.write(place + '\n\n')

    def recognition(self, text, file):
        div_pattern = re.compile(r'<div class="right".*?</div>', re.DOTALL)
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
            file = open('Ess/Page' + str(self.page) + '.txt', "w", encoding='utf-8')
            self.recognition(html.text, file)
            file.close()
            self.page += 1
        self.error_file.write(time.strftime("%b %d %Y %H:%M:%S", time.localtime()))
        self.error_file.close()


if __name__ == '__main__':
    a = Ess()
    a.start()
