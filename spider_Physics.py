# -*- coding: utf-8 -*-
import re
import os
import requests
import random


header = {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, application/json, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/55.0.2883.87 UBrowser/6.2.4094.1 Safari/537.36',
}

my_headers = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) "
    "AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 '
    'Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) "
    "Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/55.0.2883.87 UBrowser/6.2.4094.1 Safari/537.36"
]


class Physics:
    def __init__(self):
        self.url = 'https://phy.sustc.edu.cn/index.php?s=/List/index/cid/33/p/'
        self.title = 'http://phy.sustc.edu.cn'
        self.page = 1
        self.max_page = 21
        if not os.path.exists('Physics'):
            os.makedirs('Physics')
        if os.path.exists('Physics/Error_message' + '.txt'):
            self.error_file = open('Physics/Error_message' + '.txt', "a", encoding='utf-8')
        else:
            self.error_file = open('Physics/Error_message' + '.txt', "w", encoding='utf-8')

    def matching(self, text, file):
        name_pattern = re.compile(r'">.*?</a>')
        url_pattern = re.compile(r'<a href=.*?">')
        time_pattern = re.compile(r'time">.*?</span>')
        detail_pattern = re.compile(r'<span>.*?</span>')
        speaker = 'None'
        place = 'None'
        time = 'None'
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
            time = re.search(time_pattern, text).group()[6:-7]
            time = time[:4]
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
                        time += ' ' + item[3:-1]
        file.write(name + '\n')
        file.write(url + '\n')
        file.write(speaker + '\n')
        file.write(time + '\n')
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
        header['User_Agent'] = random.choice(my_headers)
        while self.page <= self.max_page:
            url = self.url + str(self.page) + '.html'
            try:
                html = requests.get(url, header, timeout=5)
                cookies = html.cookies
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
        self.error_file.close()
        os.remove('Physics/Error_message' + '.txt')


if __name__ == '__main__':
    a = Physics()
    a.start()
