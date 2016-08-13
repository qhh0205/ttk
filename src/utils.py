# -*- coding:gb2312 -*-

"""
A simple args parser and a color wrapper.
"""
import sys
import random
import requests
from requests.exceptions import ConnectionError, Timeout


__all__ = ['args', 'colored', 'requests_get', 'exit_after_echo']

def exit_after_echo(msg, color='red'):
    if color == 'red':
        print(colored.red(msg))
    else:
        print(msg)
    sys.exit(1)


def requests_get(url, **kwargs):
    USER_AGENTS = (
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100 101 Firefox/22.0',
        'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0',
        ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.5 (KHTML, like Gecko) '
         'Chrome/19.0.1084.46 Safari/536.5'),
        ('Mozilla/5.0 (Windows; Windows NT 6.1) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46'
         'Safari/536.5')
    )
    try:
        r = requests.get(
            url,
            timeout=12,
            headers={'User-Agent': random.choice(USER_AGENTS)}, **kwargs
        )
    except ConnectionError:
        exit_after_echo('Network connection failed.')
    except Timeout:
        exit_after_echo('timeout.')
    return r

class Args(object):

    """A simple customed args parser for `iquery`."""

    def __init__(self, args=None):
        self._args = sys.argv[1:]
        self._argc = len(self)

    def __repr__(self):
        return '<args {}>'.format(repr(self._args))

    def __len__(self):
        return len(self._args)

    @property
    def all(self):
        return self._args

    def get(self, idx):
        try:
            return self.all[idx]
        except IndexError:
            return None

    @property
    def is_null(self):
        return self._argc == 0

    @property
    def options(self):   # 获取火车票查询选项  ex: iquary -dgktz 上海  北京   返回dgktz
        """Train tickets query options."""
        arg = self.get(0)   #  -dgktz
        if arg.startswith('-') and not self.is_asking_for_help:
            return arg[1:]   # dgktz
        return ''.join(x for x in arg if x in 'dgktz')

    @property
    def is_asking_for_help(self):
        arg = self.get(0)
        if arg in ('-h', '--help'):
            return True
        return False

    @property
    def is_querying_train(self):
        if self._argc not in (3, 4):
            return False
        if self._argc == 4:
            arg = self.get(0)
            if not arg.startswith('-'):
                return False
            if arg[1] not in 'dgktz':
                return False
        return True

    @property
    def as_train_query_params(self):  # 查询参数
        opts = self.options
        if opts:
            # apped valid options to end of list
            return self._args[1:] + [opts]
        return self._args


class Colored(object):
    # 显示格式: \033[显示方式;前景色;背景色m
    # 只写一个字段表示前景色,背景色默认
    RED = '\033[91m'      # 红色
    GREEN = '\033[92m'    # 绿色
    YELLOW = '\033[93m'   # 黄色
    BLUE = '\033[34m'     # 蓝色
    FUCHSIA = '\033[1;35;40m'  # 紫红色
    CYAN = '\033[36m'     # 青蓝色
    WHITE = '\033[37m'    # 白色
    NOTESTR = '\033[5;37;46m'  # 提示字符串
    #: no color
    RESET = '\033[0m'  # 终端默认颜色

    def color_str(self, color, s):
        return '{}{}{}'.format(
            getattr(self, color),
            s,
            self.RESET
        )

    def red(self, s):
        return self.color_str('RED', s)

    def green(self, s):
        return self.color_str('GREEN', s)

    def yellow(self, s):
        return self.color_str('YELLOW', s)

    def blue(self, s):
        return self.color_str('BLUE', s)

    def fuchsia(self, s):
        return self.color_str('FUCHSIA', s)

    def cyan(self, s):
        return self.color_str('CYAN', s)

    def white(self, s):
        return self.color_str('WHITE', s)

    def note_str(self, s):
        return self.color_str('NOTESTR', s)

args = Args()
colored = Colored()

