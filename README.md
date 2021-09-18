# Chinese-estate-helper

[![License: GPL](https://img.shields.io/badge/License-GPL-yellow.svg)](https://opensource.org/licenses/GPL)

## 介绍
本项目用于爬取 [链家](https://sh.lianjia.com/ditu/) 的二手房数据，进行数据分析和展示，以供买房参考。

本项目目前可以达到如下目的，更多效果目前懒得开发：

- MySQL储存二手房数据

![](/images/mysql.png)

- 查询上海徐汇漕河泾半径10公里内小区

![](/images/漕河泾半径10公里小区.png)

- 查询上海闵行区所有小区

![](/images/上海闵行小区.png)

- 查询上海市区均价

![](/images/上海市区均价.png)

- 将数据储存为excel

![](/images/excel本地存储.png)

部分为互动界面，可以直接点开链接：

[](/images/上海_闵行_d_communities_draw.html)

[](/images/上海_闵行_communities_draw.html)

[](/images/上海_districts_draw.html)

## 安装教程
如果只是需要下载链家二手房数据的话，只需要执行步骤1和2即可。

#### 1.代码开发版本为Python 3.6，请自行安装。
#### 2.安装python包
下载代码，打开终端切换至代码的根目录，安装相关的依赖包。
运行
```python3
pip install requirements.txt
``` 
#### 3.数据库安装
房产数据储存方式有两种
- 一种是使用python自带的数据库sqlite3
- 一种是使用[MySQL](https://dev.mysql.com/downloads/mysql/) 数据库

建议使用MySQL数据库，功能会更全一点，操作起来更方便。

**[MySQL](https://dev.mysql.com/downloads/mysql/) 的安装步骤：**
- 首先，我使用的是MySQL 8，可以直接从官网下载，网上有各种安装教程。
- 配置你的MySQL数据库，添加 ```src/configuration/mysql_cfg.py```文件。
<br> ```src/configuration/mysql_cfg.py``` 的文件内容可以参考以下格式:
```python3
class MySQLCFG(object):
    HOST = 'localhost'
    PORT = 3306
    USER = "root"
    PASSWORD = "xxx"
    DB = "xxx"
``` 
- 同时，在MySQL中创建相应的数据库```create database xxx;```。

#### 4.安装[ABuilder](https://github.com/lizhenggan/ABuilder) 
[ABuilder](https://github.com/lizhenggan/ABuilder) 可以对MySQL进行链式查询，可以直接键入```pip install a-sqlbuilder```进行安装，但是需要相关配置。
<br>你需要写一个ABuilder的配置文件 ```tasks/database.py``` 。
<br>具体教学你可以直接查看[ABuilder的github页面](https://github.com/lizhenggan/ABuilder).

#### 5.注册[地图api](https://lbs.amap.com/) （此步骤非必须）
- 如果你想使用本项目全部的功能，你还需要配置高德API，这能让你输入一个地址，获得地址相应的地理编码。
<br>例如：输入"上海市 徐汇区 漕河泾" 可以获得 ['31.164680', '121.403738']
- 如何配置高德api网上有详细教程，需要去[高德api官网](https://lbs.amap.com/) 免费注册。
- 注册完后需要在```src/configuration```路径下添加配置文件```src/configuration/gaode_api_cfg.py```。
<br> ```src/configuration/gaode_api_cfg.py``` 的文件内容可以参考以下格式:
```python3
class GaodeApiCFG(object):
    KEY = '你在高德注册的Key'
``` 


## 使用说明

代码的[tasks](tasks)目录底下为相关的代码，

- ```tasks/lianjia_sqlite_task.py```：下载链家二手房数据，存入本地sqlite3数据库中。
- ```tasks/lianjia_mysql_task.py```：下载链家二手房数据，存入本地MySQL数据库中。
- ```tasks/basic_task.py```和```tasks/search_communities.py```：对二手房数据进行数据分析和可视化。

## 主要功能

#### 1.基于[Lianjia](https://github.com/xjkj123/Lianjia) 的链家二手房数据爬取。
**LianJiaSpider速度一分钟1000+**
+ 利用[此网页](https://sh.lianjia.com/ditu/)接口实现功能 
+ 此接口通过网页js脚本计算出get所需参数，攻破了此难点，接口调用次数无限，速度不限，上海市100000+数据不会被反爬

#### 2.基于[MySQL数据库](https://dev.mysql.com/downloads/mysql/) 本地存储数据。
+ 与数据库交互非常方便

        +--------------+------------+
        | name         | unit_price |
        +--------------+------------+
        | 黄浦         |      80305 |
        | 徐汇         |      90880 |
        ......
#### 3.二手房数据分析。
+ 有关于district, community, house的数据结构。可以执行按名称过滤，筛选等数据库难以执行的操作。
+ 可以将过滤后的二手房数据储存为本地的EXCEL文件。（这个功能没有完全开发完，只写了community的）。

#### 4.数据可视化。
+ 基于[folium](http://python-visualization.github.io/folium/) 绘制地图，展示数据。
+ 基于[folium](http://python-visualization.github.io/folium/) 绘制[热力图](https://zhuanlan.zhihu.com/p/44355878) ，绘制数据分析结果。

#### 5.其他特性。
+ 本地缓存(local cache)
+ 日志打印(logging)
+ 信息采集
+ 一些脚手架

## 提示
- 从链家获取数据接口的代码参考[Lianjia](https://github.com/xjkj123/Lianjia) 。
- 代码仅供学习与交流，不可商用。
