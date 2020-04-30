# 假期列表
from datetime import datetime

holidaylist = [
    '2020-01-01', '2020-01-24', '2020-01-25', '2020-01-26', '2020-01-27', '2020-01-28', '2020-01-29', '2020-01-30',
    '2020-04-04', '2020-04-05', '2020-04-06', '2020-05-01', '2020-05-02', '2020-05-03', '2020-05-04', '2020-05-05',
    '2020-06-25', '2020-06-26', '2020-06-27', '2020-10-01', '2020-10-02', '2020-10-03', '2020-10-04', '2020-10-05',
    '2020-10-06', '2020-10-07', '2020-10-08']

# 调休列表
dayofflist = [
    '2020-01-19', '2020-02-01', '2020-04-26', '2020-05-09', '2020-06-28', '2020-09-27', '2020-10-10']


def isholiday(timestr):
    dt = datetime.strptime(timestr, '%Y-%m-%d')
    if timestr in holidaylist:
        return True
    elif timestr in dayofflist:
        return False
    elif dt.weekday() > 4:
        return True
    else:
        return False


if __name__ == "__main__":
    print(isholiday('2020-04-26'))
