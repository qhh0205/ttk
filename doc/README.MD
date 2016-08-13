
# ttk火车票查询工具
***
####功能说明:
    本程序提供了命令行火车票查询功能,以表格的形式显示查询
    的结果.
***
***
####使用说明:
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
***
***
####图文教程:
![image](https://github.com/qianghaohao/ttk/raw/master/image/result.png)
***
***
####关于安装:
    本工具已经用pyinstaller工具打包成exe格式,无需专门安装,可以
    直接在工程目录下的bin目录找到exe文件执行,需要注意的是bin目
    录中的datas文件夹必须要和ttk.exe文件在同一目录.
***
***
####关于本工具
[https://github.com/protream/iquery](https://github.com/protream/iquery)
    本程序参考自:https://github.com/protream/iquery,在此基础
    上做了一些改进:
             1.从py3.x改成了py2.x
             2.可以支持票价查询
             3.windows下支持简体中文
	     4.程序中编码统一为GB2312
***

***
####TO-DO:
    日后有时间了写个成绩查询工具,集成到iquery,可以查询各个高校的成绩,以
    表格的形式显示出成绩,这么做主要是为了方便成绩的查询,因为现在大多高校
    网站登录都需要输入验证码,还有其他选择按钮,而且登录进去还有跳转好几个
    页面才能查到最终需要的成绩,所以如果实现了成绩查询,将会方便很多,直接一
    条命令下去,全部成绩一览无余.
***
