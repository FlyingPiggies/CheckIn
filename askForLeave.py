import re
from datetime import datetime

import requests

import setting

login_host = 'http://dcone.digitalchina.com'

portal_host = 'http://dcone.portal.digitalchina.com'

redirect_host = 'http://10.128.180.24:1096'


def web_login(s):
    login_url = '/pkmslogin.form'

    s.headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C;'
                      ' .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729)'
    }

    payload = {'username': setting.Username, 'password': setting.Password, 'login-form-type': 'pwd'}
    response = s.post(login_host + login_url, data=payload)

    # js reload location : http://dcone.digitalchina.com/portal
    if response.status_code == 200:
        r = s.get(login_host + "/portal/")
        # js reload location :  http://dcone.portal.digitalchina.com/login/Login.jsp?logintype=1
        if r.status_code == 200:
            res = s.get(portal_host + '/login/Login.jsp?logintype=1')
            if res.status_code == 200:
                pass
            else:
                raise Exception('redirect failed')
        else:
            raise Exception('redirect failed')
    else:
        raise Exception('login failed')


def get_month():
    return datetime.now().strftime('%Y%m')


def get_aspxauth(s):
    auth_url = '/login.aspx?userno=jinqu&type=F0723A8BF23ADF53&flag=kq'
    response = s.get(redirect_host + auth_url)
    if response.status_code == 200:
        pass
    else:
        raise Exception('get auth token failed')


def get_leave_form(s):
    leave_form_url = '/ChuqinTableV1.aspx?UserNo=9FDCB25C8D8112FF7326030F47600CB2&KqDate=' + get_month()

    response = s.get(redirect_host + leave_form_url)

    if response.status_code == 200:
        pass
    else:
        raise Exception('get leave form failed')

    return response.text


session = requests.Session()
web_login(session)
get_aspxauth(session)
html = get_leave_form(session)

pat = 'id=\"RadGrid1_ctl00_ctl(\d+)_lblBeatDate\">([\d-]+)'

its = re.findall(pat, html)
for a, b in its:
    print(b)