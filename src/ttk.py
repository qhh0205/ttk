# coding:gb2312
#
# 主程序入口
# 火车票查询工具:本程序参考自https://github.com/protream/iquery,在此基础
# 上做了一些改进:
#            1.从py3.x改成了py2.x
#            2.*可以支持票价查询*
#            3.使用colorama模块在终端显示彩色字符,可以很好地兼容windows
#            4.程序中编码统一为GB2312,很好地支持中文
#
# Filename: ttk.py
# Author: qianghaohao(CodeNutter)
# Mail: codenutter@foxmail.com
# ProjectName: ttk
#

from core import cli

if __name__ == '__main__':
    cli()
