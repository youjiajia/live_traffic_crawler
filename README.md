# 从爬取的百度地图实时交通图中获取交通热力状态，并获取每个拥堵路段的经纬度

## 环境安装
在项目目录下运行`./install.sh`

## 项目运行

### 后台运行django

在百度目录下运行`python manage.py runserver &`

### 定时爬取任务
借助Linux下的crontab工具， 在/etc/crontab文件中加入两行:

    `1 *     * * *   root    /root/baidu/road/data/start.sh`（换成项目路径）
    `59 *    * * *   root    /root/baidu/road/data/kill.sh`（换成项目路径）

### 项目数据
项目数据存放在sqlite中，爬取到每小时交通路段拥堵情况，每条记录包括，该点瓦片坐标，该点经纬度，该点路况。

## 项目思路
整体思路来源于http://www.jiazhengblog.com/blog/2011/07/02/289/