import setting

host = 'https://mydch.digitalchina.com:8443'


def get_config(s):
    s.headers = {
        'Timezone': 'GMT + 8',
        'User-Agent': '神州e家E-Mobile 6.5.11 (iPhone; iOS 13.1.2; zh_CN)'.encode('utf-8'),
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    }
    url = "/client.do?method=getconfig&clientver=6.5.11&clienttype=iPhone&language=zh-Hans&country=CN"
    r = s.get(host + url, verify=False)
    if r.status_code == 200:
        pass
    else:
        raise Exception('Can\'t get config')


def login(s):
    login_url = '/client.do?method=login' \
                '&udid=C9C98907-862A-41D4-993D-E31CDB27292A' \
                '&token=b2d2224d7b47e3f5a835b9a3a5fe71f6161ecec302ca2515a504bcdab95b9487' \
                '&language=zh-Hans' \
                '&country=CN' \
                '&isneedmoulds=1' \
                '&clienttype=iPhone' \
                '&clientver=6.5.11' \
                '&clientos=iOS' \
                '&clientosver=13.1.2' \
                '&authcode=' \
                '&dynapass=' \
                '&tokenpass=' \
                '&clientChannelId=' \
                '&clientuserid=101d85590922fbc1ae1'

    payload = {'loginid': setting.Username, 'password': setting.Password, 'isFromSunEmobile': '1'}

    r = s.post(host + login_url, data=payload, verify=False)

    if r.status_code == 200:
        pass
    else:
        raise Exception('Can\'t login')