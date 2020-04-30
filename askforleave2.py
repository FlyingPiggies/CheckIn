import re
from datetime import datetime

import requests
from lxml import etree

import setting

host = 'http://10.128.180.24:1096'


def getlogintoken(s, login_url):
    # //input[ @ type = 'hidden'] /@value
    r = s.get(host + login_url)
    root = etree.HTML(r.content)
    values = root.xpath('//input[@type="hidden"]/@value')
    return tuple(values)


def web_login(s):
    login_url = '/login.aspx'
    VIEWSTATE, VIEWSTATEGENERATOR, EVENTVALIDATION = getlogintoken(s, login_url)

    s.headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C;'
                      ' .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729)'
    }

    payload = {'__VIEWSTATE': VIEWSTATE,
               '__VIEWSTATEGENERATOR': VIEWSTATEGENERATOR,
               '__EVENTVALIDATION': EVENTVALIDATION,
               'txtUserName': setting.Username,
               'hfdUserName': '',
               'txtUserPwd': setting.Password,
               'Button1': '登陆'}
    response = s.post(host + login_url, data=payload)

    if response.status_code == 200:
        pass
    else:
        raise Exception('login failed')


def get_month():
    return datetime.now().strftime('%Y%m')


def get_userno(s):
    # jinqu : 9FDCB25C8D8112FF7326030F47600CB2
    r = s.get(host + '/RigthShow.aspx')
    if r.status_code == 200:
        pat = 'UserNo=(\w+)'
        its = re.findall(pat, r.text)
        return its[0]
    else:
        raise Exception('get userno failed')


def get_leave_form(s):
    leave_form_url = '/ChuqinTableV1.aspx?UserNo=' + get_userno(s) + '&KqDate=' + get_month()

    response = s.get(host + leave_form_url)

    if response.status_code == 200:
        pass
    else:
        raise Exception('get leave form failed')

    return response.text


def isleave():
    session = requests.Session()
    web_login(session)
    html = get_leave_form(session)
    pat = 'id=\"RadGrid1_ctl00_ctl(\d+)_lblBeatDate\">([\d-]+)'
    its = re.findall(pat, html)
    leavelist = []
    for a, b in its:
        leavelist.append(b)

    datestr = str(datetime.now().year) + '-' + str(datetime.now().month) + '-' + str(datetime.now().day)

    return datestr in leavelist


if __name__ == '__main__':
    print(isleave())
