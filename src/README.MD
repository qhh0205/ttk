# ttk火车票查询工具
***
####功能说明:
    本程序提供了命令行下火车票查询功能,以表格的形式显示查询的结果.
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
        入20160111,这样解析出来就是2016-1-11,其他歧义类似处理.
***
####显示效果:
**-------->Windows10:**
![image](https://github.com/qianghaohao/ttk/raw/master/image/result.png)
**-------->Windows7:**
![image](https://github.com/qianghaohao/ttk/raw/master/image/ttk_win7.png)
***
####关于安装:
    本工具已经用pyinstaller工具打包成exe格式,无需专门安装,可以
    直接在工程目录下的bin目录找到exe文件执行,需要注意的是bin目
    录中的datas文件夹必须要和ttk.exe文件在同一目录.
***
####开发平台及工具:
    1.开发平台:windows10,python2.7.11
    2.开发工具:pycharm IDE,python2.7.11
***
####TO-DO:
    日后有时间了写个成绩查询工具,集成到iquery,可以查询各个高校的成绩,以
    表格的形式显示出成绩,这么做主要是为了方便成绩的查询,因为现在大多高校
    网站登录都需要输入验证码,还有其他选择按钮,而且登录进去还要跳转好几个
    页面才能查到最终需要的成绩,所以如果实现了成绩查询,将会方便很多,直接一
    条命令下去,全部成绩一览无余.
***
####关于本工具:
######本程序参考自:[https://github.com/protream/iquery](https://github.com/protream/iquery)
	在此基础上做了一些改进:
               1.从py3.x改成了py2.x
               2.*可以支持票价查询*
               3.使用colorama模块在终端显示彩色字符,可以很好地兼容windows
               4.程序中编码统一为GB2312,很好地支持中文
    通过python的requests模块向12306发送https请求,需要注意的是请求时一定要
    忽略ssl认证--设置get请求参数的verify参数为False,要不然请求会失败,然后
    将服务器响应的json数据解析出来得到结果,通过prettytable模块以表格的形式
    显示出来.字体的颜色是通过自己封装的Colored类来实现,通过转义序列实现不同
    颜色的显示,转义序列以ESC开头.在开发过程中由于全部源文件使用统一的GB2312,
    因此可以在windows下正常运行.如果用utf-8标准,在windows除非标准输出也是utf-8,
    否则输出的是一堆乱码.考虑到windows下编码大多是GB2312标准,所以整个工程采
    用GB2312编码.
    
**声明:任何人都可以获得此代码,在此基础上任意修改,任意重新发布.如果因为使用本工具造成任何损失,本人概不负责!**
***

