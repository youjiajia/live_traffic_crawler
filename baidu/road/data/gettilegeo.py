#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   jiajia you
#   E-mail  :   hi_youjiajia@163.com
#   Date    :   16/04/29 19:11:19
#   Desc    :
#

import requests,json,time,datetime
from multiprocessing import Pool
from gevent import monkey; monkey.patch_socket()
import gevent
def filepart(getmin,getmax):
    with open('./chinascope.json','r') as chinascope:
        tilejson=json.loads(chinascope.read())
        num=0
        for x in xrange(getmin,getmax+1):
            num += 1
            onexlist=[]
            with open('./log/jc.log','a') as logfile:
                logfile.write('共需要获取{0}的瓦片，现在获取到第{1}个'.format(getmax-getmin+1,num))
                logfile.write('\n')
            # for y in xrange(int(tilejson['ymin']),int(tilejson['ymax'])+1):
            #获取南京市数
            # for y in xrange(7111,7463+1):
            #获取云南省的数据
            for y in xrange(4675,6615+1):
                #time.sleep(1)
                nowtime=time.time()
                oneurl='http://its.map.baidu.com:8002/traffic/TrafficTileService?time={0}&level=17&x={1}&y={2}'.format(nowtime,x,y)
                try:
                    try:
                        response=requests.get(url=oneurl,timeout=10)
                    except:
                        response=requests.get(url=oneurl,timeout=10)
                except Exception,e:
                    with open('./log/scope.log','a') as logfile:
                        logfile.write('{0},{1}'.format(x,y))
                        logfile.write('\n')
                        # logfile.write(str(e))
                        # logfile.write('\n')
                    continue
                if response.text!='':
                    onexlist.append('{0},{1}'.format(x,y))
            with open('ynalltiles','a') as alltilefile:
                for onecontent in onexlist:
                    alltilefile.write(onecontent)
                    alltilefile.write('\n')
def onegevent(start):
    geventlist=[]
    x=start
    for jc in xrange(1,11):
        if jc !=1:
            x += 19
        y = x + 18
        geventlist.append(gevent.spawn(filepart,x,y))
    gevent.joinall(geventlist)
if __name__=='__main__':
    starttime=str(datetime.datetime.now())
    p = Pool(processes=10)
    x = 21206
    for num in xrange(0,10):
        with open('./log/jc.log','a') as logfile:
            logfile.write('进程'+str(num)+'开始启动')
            logfile.write('\n')
        start=x+num*19*10
        p.apply_async(onegevent,args=(start,))
    p.close()
    p.join()
    endtime=str(datetime.datetime.now())
    print '开始时间为{0}，结束时间为{1}'.format(starttime,endtime)
