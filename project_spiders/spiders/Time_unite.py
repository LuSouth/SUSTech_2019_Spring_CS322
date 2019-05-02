import re

data_change = {
    'Jan': 1,
    'Feb': 2,
    'Mar': 3,
    'Apr': 4,
    'May': 5,
    'Jun': 6,
    'Jul': 7,
    'Aug': 8,
    'Sep': 9,
    'Oct': 10,
    'Nov': 11,
    'Dec': 12
}


def unite(ori_time):
    if ori_time is None:
        return 'None'
    data_pattern = re.compile(r'[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}')
    try:
        new_time = re.search(data_pattern, ori_time).group()
    except AttributeError:
        return 'None'
    if new_time[-2] == '0' or new_time[-2] == ' ':
        new_time = new_time[:-2] + new_time[-1]
    if new_time[5] == '0' or new_time[5] == ' ':
        new_time = new_time[:5] + new_time[6:]
    return new_time


def physic(ori_time, default=None):
    if default is None:
        return 'None'
    default = unite(default)
    if ori_time.find('月') > -1:
        year = ori_time[:ori_time.find('年')]
        month = ori_time[ori_time.find('年')+1: ori_time.find('月')]
        if ori_time.find('号') > -1:
            day = ori_time[ori_time.find('月')+1: ori_time.find('号')]
        else:
            day = ori_time[ori_time.find('月') + 1: ori_time.find('日')]
        return str(year) + '-' + str(month) + '-' + str(day)
    if ori_time.find('day') > -1:
        day_pattern = re.compile(r'[0-9]{1,2}[trvns ]')
        month_pattern = re.compile(r'[A-Z][a-z]+')
        day = re.search(day_pattern, ori_time).group()[:-1]
        month = int(default.split('-')[1])
        m = re.findall(month_pattern, ori_time)
        for item in m:
            if 'day' not in item:
                month = data_change[item[:3]]
        if month == 1 and default[5:7] == '12':
            year = int(default[0:4]) + 1
        else:
            year = int(default[0:4])
        return str(year) + '-' + str(month) + '-' + str(day)
    return default


def ess(ori_time):
    if ori_time is None:
        return 'None'
    if ori_time.find('月') > -1:
        if ori_time.find('年') > -1:
            year = ori_time[:ori_time.find('年')]
        else:
            year = 2018
        month = ori_time[ori_time.find('年')+1: ori_time.find('月')]
        if ori_time.find('号') > -1:
            day = ori_time[ori_time.find('月')+1: ori_time.find('号')]
        else:
            day = ori_time[ori_time.find('月') + 1: ori_time.find('日')]
        return str(year).strip(' ') + '-' + month.strip(' ') + '-' + day.strip(' ')
    return 'None'


def ese(ori_time):
    if ori_time is None:
        return 'None'
    if ori_time.find('月') > -1:
        if ori_time.find('年') > -1:
            year = ori_time[:ori_time.find('年')]
        else:
            return 'None'
        month = ori_time[ori_time.find('年')+1: ori_time.find('月')]
        if ori_time.find('号') > -1:
            day = ori_time[ori_time.find('月')+1: ori_time.find('号')]
        else:
            day = ori_time[ori_time.find('月') + 1: ori_time.find('日')]
        return str(year).strip(' ') + '-' + month.strip(' ') + '-' + day.strip(' ')
    return 'None'


def bme(ori_time, year):
    if ori_time.find('月') > -1:
        if ori_time.find('年') > -1:
            year = ori_time[:ori_time.find('年')]
        month = ori_time[ori_time.find('年')+1: ori_time.find('月')]
        if ori_time.find('号') > -1:
            day = ori_time[ori_time.find('月')+1: ori_time.find('号')]
        else:
            if ori_time.find('日') > -1:
                day = ori_time[ori_time.find('月') + 1: ori_time.find('日')]
            else:
                day = ori_time[ori_time.find('月') + 1: ori_time.find('（')]
        return str(year).strip(' ') + '-' + month.strip(' ') + '-' + day.strip(' ')
    for item in data_change.keys():
        if ori_time.find(item) != -1:
            month = data_change[item]
            day_pattern = re.compile(r'[0-9]{1,2}[^0-9ap:]')
            day = re.search(day_pattern, ori_time).group()[:-1]
            return str(year).strip(' ') + '-' + str(month) + '-' + day.strip(' ')
    return 'None'


def bio(ori_time, de_year):
    month = ori_time[:ori_time.find('月')]
    day = ori_time[ori_time.find('月')+1: ori_time.find('日')]
    return str(de_year)+ '-' + month.strip(' ') + '-' + day.strip(' ')


def fin(ori_time):
    ori_time.replace(' ', '')
    if ori_time is None:
        return 'None'
    if ori_time.find('月') > -1:
        if ori_time.find('年') > -1:
            year = ori_time[:ori_time.find('年')]
        else:
            return 'None'
        month = ori_time[ori_time.find('年')+1: ori_time.find('月')]
        if ori_time.find('号') > -1:
            day = ori_time[ori_time.find('月')+1: ori_time.find('号')]
        else:
            day = ori_time[ori_time.find('月') + 1: ori_time.find('日')]
        return str(year).strip(' ') + '-' + month.strip(' ') + '-' + day.strip(' ')
    pattern = re.compile(r'[0-9]{4}.[0-9]{1,2}.[0-9]{1,2}')
    try:
        tmp = re.search(pattern, ori_time).group()
        return tmp.replace('.', '-')
    except AttributeError:
        pass
    return 'None'


def med(ori_time):
    if ori_time is None:
        return 'None'
    if ori_time.find('月') > -1:
        if ori_time.find('年') > -1:
            year = ori_time[:ori_time.find('年')]
        else:
            return 'None'
        month = ori_time[ori_time.find('年')+1: ori_time.find('月')]
        if ori_time.find('号') > -1:
            day = ori_time[ori_time.find('月')+1: ori_time.find('号')]
        else:
            day = ori_time[ori_time.find('月') + 1: ori_time.find('日')]
        return str(year).strip(' ') + '-' + month.strip(' ') + '-' + day.strip(' ')
    if ori_time.find('/') != -1:
        ori_time = ori_time.replace('/', '-')
        return unite(ori_time)
    return 'None'
