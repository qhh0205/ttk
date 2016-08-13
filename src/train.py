# -*- coding:gb2312 -*-

"""
# The program entrance.
Train tickets query and display. The datas come
from:
    www.12306.cn
"""

import os
import re
import sys
reload(sys)
sys.setdefaultencoding('GB2312')
import datetime
from collections import OrderedDict
from prettytable import PrettyTable
from utils import colored, requests_get, exit_after_echo
from Q2B_and_B2Q import *

__all__ = ['query']

QUERY_URL = 'https://kyfw.12306.cn/otn/lcxxcx/query'    # 余票查询
PRICE_QUERY_URL = 'https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice'  # 票价查询
# ERR
FROM_STATION_NOT_FOUND = 'From station not found.'
TO_STATION_NOT_FOUND = 'To station not found.'
INVALID_DATE = 'Invalid query date.'
TRAIN_NOT_FOUND = 'No result.'
NO_RESPONSE = 'Sorry, server is not responding.'


class TrainsCollection(object):

    """A set of raw datas from a query."""

    headers = '车次 车站 时间 历时 商务座 特等座 一等座 二等座 高级软卧 软卧 硬卧 软座 硬座 无座 其他'.split()

    def __init__(self, rows, opts, date, from_station, to_station):
        self._rows = rows
        self._opts = opts
        self._date = date
        self._from_station = from_station
        self._to_station = to_station
        cnt = 0     #  记录车次个数
    def __repr__(self):
        return '<TrainsCollection size={}>'.format(len(self))

    def __len__(self):
        return len(self._rows)

    def _get_duration(self, row):
        duration = row.get('lishi').encode('GB2312').replace(':', '小时') + '分钟'
        # take 0 hour , only show minites
        if duration.startswith('00'):   #  小于一小时  ex: 00小时23分钟--->23分钟
            return duration[4:]
        # take <10 hours, show 1 bit
        if duration.startswith('0'):  #  小于十小时  ex: 05小时38分钟--->5小时38分钟
            return duration[1:]
        return duration

    def _build_params(self, row):
        """票价请求参数, 返回有序字典,字典添加顺序和采点时参数顺序必须一致,要不然请求会失败
        """
        d = OrderedDict()
        d['train_no'] = row.get('train_no')
        d['from_station_no'] = row.get('from_station_no')
        d['to_station_no'] = row.get('to_station_no')
        d['seat_types'] = row.get('seat_types')
        d['train_date'] = self._date
        return d

    #  --------------- 返回票价数据样例 -----------------
    # {"validateMessagesShowId": "_validatorMessage",
    #  "status": true,
    #  "httpstatus": 200,
    #  "data": {"3": "3105",
    #           "A1": "?180.5",
    #           "1": "1805",
    #           "A4": "?488.5",
    #           "A3": "?310.5",
    #           "4": "4885",
    #           "OT": [],
    #           "WZ": "?180.5",
    #           "train_no": "870000K35963"
    #           },
    #  "messages": [],
    #  "validateMessages": {}}
    # --------------------------------------------------

    def _get_price(self, row):       # 获取每列车不同席别的票价,返回一个列表
        params = self._build_params(row)
        r = requests_get(PRICE_QUERY_URL, params=params, verify=False)
        try:
            rows = r.json()['data']  # 得到json查询结果
        except KeyError:
            rows = {}
        except TypeError:
            exit_after_echo(NO_RESPONSE)
        return rows

    def replace_and_append(self, s, c='', a='元'):
        '''
         此函数可以将给定字符串的第一个字符替换成c,然后
         在末尾追加一个字符串a.如果s为空则不追加任何字符串.
         默认追加 '元'
         将给定字符串s中的第一个字符替换成字符c.
         由于如果在字符串中含有gb2312无法编码的
         字符,输出将会报错.因此需要把其替换成gb2312
         能编码的字符. 在此替换后在附加了一个字符串.
        :param s: 待替换字符串
        :param c: 目标字符
        :param a: 追加字符串
        :return: 返回替换后的字符串
        '''

        try:
            result = ''
            if s:
                result = re.sub('^.', c, s)
                result = result + a
            return colored.yellow(result)
        except TypeError:
            pass
        except:
            pass

    @property
    def trains(self):
        """Filter rows according to `headers`"""
        for row in self._rows:  #  self._rows:列表类型,每个元素为一个字典,代表一个车次
            train_no = row.get('station_train_code')
            initial = train_no[0].lower()   # 车次首次母  ex:  G851--->g
            if not self._opts or initial in self._opts:   #  过滤车次种类
                # '车次 车站 时间 历时 商务座 特等座 一等座 二等座 高级软卧 软卧 硬卧 软座 硬座 无座 其它'
                train = [
                    # Column: '车次'
                    train_no,
                    # Column: '车站'
                    '\n'.join([
                        colored.green(row.get('from_station_name').encode('GB2312')),
                        colored.red(row.get('to_station_name').encode('GB2312'))
                    ]),
                    # Column: '时间'
                    '\n'.join([
                        colored.green(row.get('start_time')),
                        colored.red(row.get('arrive_time')),
                    ]),
                    # Column: '历时'
                    self._get_duration(row),
                    # Column: '商务'
                    row.get('swz_num'),
                    # Column: '特等'
                    row.get('tz_num'),
                    # Column: '一等'
                    row.get('zy_num'),
                    # Column: '二等'
                    row.get('ze_num'),
                    # Column: '高级软卧'
                    row.get('gr_num'),
                    # Column: '软卧'
                    row.get('rw_num'),
                    # Column: '硬卧'
                    row.get('yw_num'),
                    # Column: '软座'
                    row.get('rz_num'),
                    # Column: '硬座'
                    row.get('yz_num'),
                    # Column: '无座'
                    row.get('wz_num'),
                    # Column: '其它'
                    row.get('qt_num')
                ]
                # ---------通过采点得到席别对应的编号 ---------------
                #               商务座: A9
                #               特等座: P
                #               一等座: M
                #               二等座: O
                #               高级软卧: A6
                #               软卧: A4
                #               硬卧: A3
                #               软座: A2
                #               硬座: A1
                #               无座: WZ
                #               其他: OT[]
                # -------------------------------------------------
                price_dict = self._get_price(row)   #  获取票价数据
                try:
                    ot_str = self.replace_and_append('\n'.join(price_dict.get('OT')), '')
                except TypeError:
                    ot_str = ''
                price = [          # 票价列表
                    colored.yellow('票价'),
                    '',
                    '',
                    '',
                    # 由于从服务器获取到的字符从中第一个字符是'￥',这个字符
                    # 在GB2312编码中是无法编码的,在处理过程中会报错,因此需要
                    # 将第一个字符替换掉,在此用空字符替换,表示删除第一个字符,
                    # 然后追加 '元' 字符串,表示人民币
                    #  商务
                    self.replace_and_append(price_dict.get('A9', '')),
                    #  特等
                    self.replace_and_append(price_dict.get('P', '')),
                    #  一等
                    self.replace_and_append(price_dict.get('M', '')),
                    # 二等
                    self.replace_and_append(price_dict.get('O', '')),
                    # 高级软卧
                    self.replace_and_append(price_dict.get('A6', '')),
                    # 软卧
                    self.replace_and_append(price_dict.get('A4', '')),
                    # 硬卧
                    self.replace_and_append(price_dict.get('A3', '')),
                    # 软座
                    self.replace_and_append(price_dict.get('A2', '')),
                    # 硬座
                    self.replace_and_append(price_dict.get('A1')),
                    # 无座
                    self.replace_and_append(price_dict.get('WZ', '')),
                    # 其他
                    ot_str
                ]
                data_list = [train, price]
                yield data_list                # 返回车票信息和票价信息

    def get_table_header(self):
        '''
        打印表格标题: ex: 子长->西安(2016年08月17日 周三)
        :return:无返回值
        '''
        week_dict = {
            'Mon': '周一',
            'Tue': '周二',
            'Wed': '周三',
            'Thu': '周四',
            'Fri': '周五',
            'Sat': '周六',
            'Sun': '周日'
        }
        date = datetime.datetime.strptime(self._date, '%Y-%m-%d')
        date_str = date.strftime('%Y年%m月%d日 %a')
        date_str = date_str.replace(date_str[-3:], week_dict[date_str[-3:]])
        header = self._from_station + '->' + self._to_station + '(' + date_str + ')'
        print '\n%92s' % colored.red(header)

    def note_str(self, note_str):
        temp_str = '%-139s' % note_str
        print colored.note_str(temp_str)

    def pretty_print(self):
        """Use `PrettyTable` to perform formatted outprint."""
        self.note_str('正在努力加载数据中......')
        pt = PrettyTable()
        pt.encoding = 'GB2312'   # 设置prettytable编码方式,要不然在windows下无法打印中文
        if len(self) == 0:
            pt._set_field_names(['Sorry,'])
            pt.add_row([TRAIN_NOT_FOUND])
        else:
            pt._set_field_names(self.headers)
            for train in self.trains:
                pt.add_row(train[0])
                pt.add_row(train[1])
        self.note_str('数据加载完毕......')
        self.get_table_header()
        print(pt)


class TrainTicketsQuery(object):

    """Docstring for TrainTicketsCollection. """

    def __init__(self, from_station, to_station, date, opts=None):

        self.from_station = from_station
        self.to_station = to_station
        self.date = date
        self.opts = opts

    def __repr__(self):
        return 'TrainTicketsQuery from={} to={} date={}'.format(
            self.from_station, self.to_station, self.date
        )

    @property
    def stations(self):
        filepath = os.path.join(    #  获取车站数据文件名
            os.getcwd(),
            r'datas', r'stations.dat'
        )
        d = {}
        with open(filepath, 'r') as f:
            for line in f.readlines():
                name, telecode = line.split()
                d.setdefault(name, telecode)      # 将车站数据加载到字典
        return d

    @property
    def _from_station_telecode(self):
        # import chardet
        # print chardet.detect(self.from_station)   #  检查输入编码--调试用
        code = self.stations.get(self.from_station)
        if not code:
            exit_after_echo(FROM_STATION_NOT_FOUND)
        return code

    @property
    def _to_station_telecode(self):
        code = self.stations.get(self.to_station)
        if not code:
            exit_after_echo(TO_STATION_NOT_FOUND)
        return code

    @property
    def _valid_date(self):
        """Check and return a valid query date."""
        date = self._parse_date(self.date)

        if not date:
            exit_after_echo(INVALID_DATE)

        try:
            date = datetime.datetime.strptime(date, '%Y%m%d')
        except ValueError:
            exit_after_echo(INVALID_DATE)

        # A valid query date should within 50 days.
        offset = date - datetime.datetime.today()
        if offset.days not in range(-1, 50):
            exit_after_echo(INVALID_DATE)

        return date.strftime('%Y-%m-%d')
        # return datetime.date.strftime(date, '%Y-%m-%d')

    @staticmethod
    def _parse_date(date):
        """Parse from the user input `date`.

        e.g. current year 2016:
           input 6-26, 626, ... return 2016626
           input 2016-6-26, 2016/6/26, ... retrun 2016626

        This fn wouldn't check the date, it only gather the number as a string.
        """
        result = ''.join(re.findall('\d', date))
        l = len(result)

        # User only input month and day, eg 6-1, 6.26, 0626...
        if l in (2, 3, 4):
            # year = str(datetime.today().year)
            year = str(datetime.date.today().year)
            return year + result   # 转换成年月日形式  ex:423--->2016423

        # User input full format date, eg 201661, 2016-6-26, 20160626...
        if l in (6, 7, 8):
            return result

        return ''

    def _build_params(self):
        """Have no idea why wrong params order can't get data.
        So, use `OrderedDict` here.
        """
        d = OrderedDict()
        d['purpose_codes'] = 'ADULT'
        d['queryDate'] = self._valid_date
        d['from_station'] = self._from_station_telecode
        d['to_station'] = self._to_station_telecode
        return d

    def query(self):

        params = self._build_params()

        r = requests_get(QUERY_URL, params=params, verify=False)

        try:
            rows = r.json()['data']['datas']   # 得到json查询结果
        except KeyError:
            rows = []
        except TypeError:
            exit_after_echo(NO_RESPONSE)
        query_date = self._valid_date
        return TrainsCollection(rows, self.opts, query_date, self.from_station, self.to_station)


def query(params):
    """`params` is a list, contains `from`, `to`, `date`."""

    return TrainTicketsQuery(*params).query()
