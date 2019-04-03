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
        self.department = 'Ess'
        if not os.path.exists(self.department):
            os.makedirs(self.department)
        self.error_file = open(self.department + '/Error_message' + '.txt', "w", encoding='utf-8')
        self.file_all = open(self.department + '/' + self.department + '_all.csv', "w", encoding='utf-8')

    def matching(self, text):
        name_pattern = re.compile(r'html">.*?</a>')
        url_pattern = re.compile(r'<a href=.*?">')
        detail_pattern = re.compile(r'<p.*?</p>')
        speaker = 'None'
        place = 'None'
        stime = 'None'
        try:
            name = re.search(name_pattern, text).group()[6:-4]
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
            item = Headers.delect_bracket(item)
            if item.find("演讲者") > -1:
                speaker = item[item.find("演讲者")+4:]
            if item.find("时间") > -1:
                if item.find("日", 0, 15) > -1:
                    stime = item[item.find("时间")+3:item.find("日")]
                if item.find("号", 0, 15) > -1:
                    stime = item[item.find("时间") + 3:item.find("号")]
            if item.find("地点") > -1:
                place = item[item.find("地点")+3:item.find("演讲者")-3]
        if stime.find("年") == -1:
            stime = "2018年" + stime
        if stime[-2] == '月':
            stime = stime[:-1] + '0' + stime[-1]
        if stime[-5] == '年':
            stime = stime[:-4] + '0' + stime[-4:]
        stime = stime[:4] + '-' + stime[5:7] + '-' + stime[8:]
        if speaker == '':
            speaker = 'None'
        if place == '':
            place = 'None'
        content = "'" + name + "'," \
            "'" + url + "'," \
            "'" + speaker + "'," \
            "'" + stime + "'," \
            "'" + self.department + "'," \
            "'" + place + "',\n"
        self.file_all.write(content)

    def recognition(self, text):
        div_pattern = re.compile(r'<div class="right".*?</div>', re.DOTALL)
        try:
            m = re.findall(div_pattern, text)
            num = 0
            for item in m:
                num += 1
                self.error_file.write('Matching Page' + str(self.page) + ' NO.' + str(num) + '\n')
                self.matching(item)
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
            self.recognition(html.text)
            self.page += 1
        self.error_file.write(time.strftime("%b %d %Y %H:%M:%S", time.localtime()))
        self.error_file.close()
        self.file_all.close()


if __name__ == '__main__':
    a = Ess()
    a.start()
