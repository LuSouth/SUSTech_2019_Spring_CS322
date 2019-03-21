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
        self.department = 'Physics'
        if not os.path.exists(self.department):
            os.makedirs(self.department)
        self.error_file = open(self.department + '/Error_message' + '.txt', "w", encoding='utf-8')
        self.file_all = open(self.department+ '/' + self.department + '_all.csv', "w", encoding='utf-8')

    def matching(self, text, file):
        name_pattern = re.compile(r'">.*?</a>')
        url_pattern = re.compile(r'<a href=.*?">')
        stime_pattern = re.compile(r'<span class="time">.*?</span>')
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
            stime = re.search(stime_pattern, text).group()
            stime = Headers.delect_bracket(stime)
            stime = stime[:4] + '-' + stime[4:6] + '-' + stime[7:]
        except AttributeError:
            self.error_file.write('Missing time\n')
            stime = None
        m = re.findall(detail_pattern, text)
        for item in m:
            item = Headers.delect_bracket(item)
            if item.find('演讲者') > -1:
                speaker = item.replace('演讲者：', '')
            else:
                if item.find('地点') > -1:
                    place = item.replace('地点：', '')
        content = '"' + name + '",' \
            '"' + url + '",' \
            '"' + speaker + '",' \
            '"' + stime + '",' \
            '"' + self.department + '",' \
            '"' + place + '",\n'
        file.write(content)
        self.file_all.write(content)

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
            file = open(self.department + '/Page' + str(self.page) + '.txt', "w", encoding='utf-8')
            self.recognition(html.text, file)
            file.close()
            self.page += 1
        self.error_file.write(time.strftime("%b %d %Y %H:%M:%S", time.localtime()))
        self.error_file.close()
        self.file_all.close()


if __name__ == '__main__':
    a = Physics()
    a.start()
