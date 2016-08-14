# -*- coding:gb2312 -*-

"""
The program entrance.
"""
import requests
from utils import args, exit_after_echo

def show_usage():
    """Usage:
    ttk [-dgktz] <from> <to> <date>

Go to `ttk -h` or `ttk --help`for more details.
"""
    pass


def cli():
    """train tickets query via command line.

Usage:
    ttk -h
    ttk --help
    ttk [-dgktz] <from> <to> <date>

Arguments:
    from             出发站
    to               到达站
    date             查询日期

Options:
    -h, --help       显示该帮助菜单.

    -dgktz           动车,高铁,快速,特快,直达
Note:
    在输入日期参数的时候注意避免歧义,比如日期2016111将会被
    解析成2016-11-01,而不是2016-01-11.要输入2016-1-11请输
    入20160111,注意解析出来就是2016-1-11,其他歧义类似处理.

"""

    if args.is_asking_for_help:
        exit_after_echo(cli.__doc__, color=None)

    elif args.is_querying_train:
        from train import query
        result = query(args.as_train_query_params)
        result.pretty_print()
    else:
        exit_after_echo(show_usage.__doc__, color=None)

