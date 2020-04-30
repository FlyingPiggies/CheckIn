import base64
import os
import random
import schedule
from datetime import datetime, timedelta
from os.path import isfile, join
from uuid import uuid4

import requests
from requests_toolbelt import MultipartEncoder

import login
import holiday2
import askforleave2

image_path = 'images'


def getBase64String(path):
    with open(path, 'rb') as f:
        base64_data = base64.b64encode(f.read())
        s = base64_data.decode()
        return s


def get_image():
    files = [f for f in os.listdir(image_path) if isfile(join(image_path, f))]
    image = files[random.randint(0, len(files) - 1)]
    return 'data:image/jpeg;base64,%s' % getBase64String(join(image_path, image))


def get_random_jd():
    return str(121.40751570813495 + random.randint(0, 10) * 0.00000000000001)


def get_random_wd():
    return str(31.183589932484683 + random.randint(0, 10) * 0.00000000000001)


def get_random_QDSJ():
    td = timedelta(minutes=random.randint(0, 10))
    randomdatetime = datetime.now() + td
    return randomdatetime.strftime('%H:%M')


def get_random_dd():
    # '上海市徐汇区钦州北路靠近上海漕河泾开发区智汇园'
    # 钦州北路1198号 上海漕河泾开发区-智汇园
    # 上海市徐汇区钦州北路靠近漕河泾科汇大厦
    return '上海市徐汇区钦州北路靠近上海漕河泾开发区智汇园'


def checkin(s):
    url = '/mobilemode/formComponentAction.jsp?action=savedata'

    form_value = {
        'datasource': '$ECOLOGY_SYS_LOCAL_POOLNAME',
        'formtype': '1',
        'tablename': 'UF_OUT_SIGN',
        'keyname': 'ID',
        'actiontype': '0',
        'billid': '',
        'workflowid': 'null',
        'workflowtitle': '%7Bworkflowname%7D%28%E8%A1%A8%E5%8D%95%E6%8F%90%E4%BA%A4%E6%B5%81%E7%A8%8B%29-%7Bcurrusername%7D-%7Bcurrdate%7D',
        'modelid': '702',
        'validateScript': 'return+check()%3B',
        'appid': '',
        'formid': '-123',
        'fieldname_QDRY': '30595',
        'fieldname_QDRQ': datetime.now().strftime('%Y-%m-%d'),
        'fieldname_QDSJ': get_random_QDSJ(),
        'fieldname_JD': get_random_jd(),
        'fieldname_WD': get_random_wd(),
        'fieldname_DD': get_random_dd(),
        'fieldname_FL1': '上下班(含驻场)',
        'fieldname_FL2': '上下班',
        'fieldname_BZ': '上下班',
        'type_BZ': 'textarea_1',
        'fieldname_ZP': get_image(),
        'type_ZP': 'photo'
    }

    m = MultipartEncoder(
        boundary=uuid4().hex,
        fields=form_value
    )

    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148/E-Mobile',
        'Content-type': m.content_type
    })

    r = s.post(login.host + url,
               data=m.to_string(),
               verify=False)

    if r.status_code == 200:
        print(r.text)
    else:
        raise Exception('Can\'t check in')


def run():
    if not holiday2.isholiday() and not askforleave2.isleave():
        session = requests.Session()
        login.get_config(session)
        login.login(session)
        checkin(session)


if __name__ == '__main__':
    schedule.every().day.at("08:50").do(run())

    while True:
        schedule.run_pending()
