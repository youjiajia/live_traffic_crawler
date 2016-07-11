#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   jiajia you
#   E-mail  :   hi_youjiajia@163.com
#   Date    :   16/05/04 16:36:40
#   Desc    :
#
from SimpleCV import Image
import time, re, os, sys, datetime,json,requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from multiprocessing import Pool
from gevent import monkey; monkey.patch_socket()
import gevent
def gotourl(url):
    """
    使用phantomjs浏览器访问本地web服务器，并把ｊｓ计算出的结果更新到数据库中去
    """
    driver = webdriver.PhantomJS('./phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
    # 设定页面加载限制时间
    driver.set_page_load_timeout(5)
    #设置页面等待时间
    driver.implicitly_wait(5)
    try:
        try:
            driver.get(url)
        except:
            driver.get(url)
        finally:
            driver.quit()
    except Exception,e:
        print e
        accesslogfile=open('./log/failedurl.log','a+')
        accesslogfile.write(url)
        accesslogfile.write("\n")
        accesslogfile.close()
def insertdata(img,tilex,tiley,onetime):
    """
    根据获取到的图片调用无界面浏览器phantomJS
    将拥堵信息通过访问浏览器的方式存入数据库
    状态为3代表严重拥堵
    状态为2代表拥堵
    状态为1代表缓行
    """
    returnstr=''
    for x in range(0,256,3):
        for y in range(0,256,3):
            imgpixel = img.getPixel(x,y)
            y=256-y
            if imgpixel != None:
                status = 0
                pixelr,pixelg,pixelb = imgpixel
                if (pixelr>184) & (pixelr<188) & (pixelg<3) & (pixelb<3):
                    status=3
                    returnstr += '{0},{1},{2},{3},{4},{5}|'.format(tilex,tiley,x,y,onetime,status)
                elif (pixelr>240) & (pixelr<245) & (pixelg>46) & (pixelg<50) & (pixelb>46) & (pixelb<50):
                    status=2
                    returnstr += '{0},{1},{2},{3},{4},{5}|'.format(tilex,tiley,x,y,onetime,status)
                elif (pixelr>253) & (pixelg>156) & (pixelg<160) & (pixelb<27) & (pixelb>23):
                    status=1
                    returnstr += '{0},{1},{2},{3},{4},{5}|'.format(tilex,tiley,x,y,onetime,status)
    if returnstr != '':
        url="http://127.0.0.1/road/getgeo/?returnstr={0}".format(returnstr)
        gotourl(url)

def getimage(x,y):
    """
    获取百度地图图片
    """
    nowtime=time.time()
    url='http://its.map.baidu.com:8002/traffic/TrafficTileService?time={0}&level=17&x={1}&y={2}'.format(nowtime,x,y)
    try:
        try:
            img=Image(url)
        except:
            img=Image(url)
        insertdata(img,x,y,nowtime)
    except Exception,e:
        print e
        with open('./log/getpic.log','a') as logfile:
            logfile.write('{0},{1}'.format(x,y))
            logfile.write('\n')
def onegevent(lines):
    otherpattern=re.compile(r'\n|\s',re.S)
    for oneline in lines:
        oneinfo=re.sub(otherpattern,'',oneline)
        if oneinfo != '':
            infolist=oneinfo.split(',')
            getimage(infolist[0],infolist[1])
def oneprocess(lines):
    geventlist=[]
    everyline=(len(lines)/10)+1
    a=None
    for jc in xrange(0,10):
        partlines=lines[jc*everyline:(jc+1)*everyline]
        geventlist.append(gevent.spawn(onegevent,partlines))
    gevent.joinall(geventlist)
def main():
    """
    主函数
    """
    with open('./log/getpic.log','wb+') as logfile:
        logfile.truncate()
    with open('./log/failedurl.log','wb+') as logfile:
        logfile.truncate()
    otherpattern=re.compile(r'\n|\s',re.S)
    njfile=open('./njalltiles','r')
    alllines=njfile.readlines()
    everyline=len(alllines)/3+1
    p = Pool(processes=3)
    for num in xrange(0,3):
        partlines=alllines[num*everyline:(num+1)*everyline]
        p.apply_async(oneprocess,args=(partlines,))
    p.close()
    p.join()
    njfile.close()
    with open('./log/getpic.log','r') as logfile:
        for oneline in logfile.readlines():
            oneinfo=re.sub(otherpattern,'',oneline)
            if oneinfo != '':
                infolist=oneinfo.split(',')
                getimage(infolist[0],infolist[1])
    with open('./log/failedurl.log','r') as logfile:
        for oneline in logfile.readlines():
            lineinfo=re.sub(otherpattern,'',oneline)
            if lineinfo != '':
                gotourl(lineinfo)
if __name__ == '__main__':
    start = str(datetime.datetime.now())
    main()
    end = str(datetime.datetime.now())
    with open('./log/time.log','a+') as logfile:
        logfile.write('本次开始时间为{0}结束时间为{1}'.format(start,end))
        piclogfile=open('./log/getpic.log','r')
        picline=len(piclogfile.readlines())
        logfile.write('\n')
        logfile.write('获取图片错误共有'+str(picline)+'个')
        piclogfile.close()
        piclogfile=open('./log/failedurl.log','r')
        picline=len(piclogfile.readlines())
        logfile.write('\n')
        logfile.write('获取本地url错误共有'+str(picline)+'个')
        piclogfile.close()
        logfile.write('\n')
