# -*- coding:utf-8 -*-
import os,re,json
from django.shortcuts import render_to_response
from baidu import settings
from django.http import HttpResponse
# from pymongo import MongoClient
from django.views.decorators.csrf import csrf_exempt
from .models import *
import sys
reload(sys)
sys.setdefaultencoding('utf8')
@csrf_exempt
def gettiles(request):
    url=os.path.join(settings.BASE_DIR,'road','data','citydata.json')
    cityfile=open(url,'r')
    cityjson=cityfile.read()
    otherpattern=re.compile('\n|\s')
    cityjson=re.sub(otherpattern,'',cityjson)
    cityfile.close()
    return render_to_response('gettiles.html',{'cityjson':cityjson})
@csrf_exempt
def updatefile(request):
    url=os.path.join(settings.BASE_DIR,'road','data','citytile.json')
    cityfile=open(url,'w')
    cityfile.write(request.read())
    cityfile.close()
    return HttpResponse('ok')
@csrf_exempt
def getallfile(request):
    url=os.path.join(settings.BASE_DIR,'road','data','citytile.json')
    scopeurl=os.path.join(settings.BASE_DIR,'road','data','cityscope.json')
    cityfile=open(url,'r')
    cityjson=json.loads(cityfile.read())
    cityfile.close()
    for onecity in cityjson['other']:
        crisistiles=onecity['b'].split(';')
        crisistiles=list(set(crisistiles))
        if '' in crisistiles:
            crisistiles.remove('')
        tilexlist=[]
        tileylist=[]
        for tilestr in crisistiles:
            tilexlist.append(int(tilestr.split(',')[0]))
            tileylist.append(int(tilestr.split(',')[1]))
        tilexlist.sort()
        tileylist.sort()
        del onecity['b']
        onecity['n']=onecity['n'].encode('utf-8')
        onecity['xmax']=tilexlist[-1]
        onecity['xmin']=tilexlist[0]
        onecity['ymax']=tileylist[-1]
        onecity['ymin']=tileylist[0]
    for onecity in cityjson['municipalities']:
        crisistiles=onecity['b'].split(';')
        crisistiles=list(set(crisistiles))
        if '' in crisistiles:
            crisistiles.remove('')
        tilexlist=[]
        tileylist=[]
        for tilestr in crisistiles:
            tilexlist.append(int(tilestr.split(',')[0]))
            tileylist.append(int(tilestr.split(',')[1]))
        tilexlist.sort()
        tileylist.sort()
        del onecity['b']
        onecity['n']=onecity['n'].encode('utf-8')
        onecity['xmax']=tilexlist[-1]
        onecity['xmin']=tilexlist[0]
        onecity['ymax']=tileylist[-1]
        onecity['ymin']=tileylist[0]
    for province in cityjson['provinces']:
        provincetiles=province['b'].split(';')
        crisistiles=list(set(provincetiles))
        if '' in crisistiles:
            crisistiles.remove('')
        tilexlist=[]
        tileylist=[]
        for tilestr in crisistiles:
            tilexlist.append(int(tilestr.split(',')[0]))
            tileylist.append(int(tilestr.split(',')[1]))
        tilexlist.sort()
        tileylist.sort()
        del province['b']
        try:
            province['n']=onecity['n'].encode('utf-8')
        except:
            province['n']=onecity['n']
        province['xmax']=tilexlist[-1]
        province['xmin']=tilexlist[0]
        province['ymax']=tileylist[-1]
        province['ymin']=tileylist[0]
        for onecity in province['cities']:
            crisistiles=onecity['b'].split(';')
            if len(crisistiles) > 1 :
                crisistiles=list(set(crisistiles))
                if '' in crisistiles:
                    crisistiles.remove('')
                tilexlist=[]
                tileylist=[]
                for tilestr in crisistiles:
                    tilexlist.append(int(tilestr.split(',')[0]))
                    tileylist.append(int(tilestr.split(',')[1]))
                tilexlist.sort()
                tileylist.sort()
                del onecity['b']
                try:
                    province['n']=onecity['n'].encode('utf-8')
                except:
                    province['n']=onecity['n']
                onecity['xmax']=tilexlist[-1]
                onecity['xmin']=tilexlist[0]
                onecity['ymax']=tileylist[-1]
                onecity['ymin']=tileylist[0]
            else:
                del onecity['b']
                try:
                    province['n']=onecity['n'].encode('utf-8')
                except:
                    province['n']=onecity['n']
                onecity['xmax']=''
                onecity['xmin']=''
                onecity['ymax']=''
                onecity['ymin']=''
    with open(scopeurl,'w') as scopefile:
        scopefile.write(json.dumps(cityjson,ensure_ascii=False))
    return HttpResponse('ok')
def getchinascope(request):
    returnjson={'xmax':0,'xmin':100000000,'ymax':0,'ymin':100000000}
    scopeurl=os.path.join(settings.BASE_DIR,'road','data','cityscope.json')
    allscopeurl=os.path.join(settings.BASE_DIR,'road','data','chinascope.json')
    with open(scopeurl,'r') as scopefile:
        filecontent=json.loads(scopefile.read())
    for onecity in filecontent['other']:
        if int(onecity['xmax']) > returnjson['xmax']:
            returnjson['xmax'] = int(onecity['xmax'])
        if int(onecity['xmin']) < returnjson['xmin']:
            returnjson['xmin'] = int(onecity['xmin'])
        if int(onecity['ymax']) > returnjson['ymax']:
            returnjson['ymax'] = int(onecity['ymax'])
        if int(onecity['ymin']) < returnjson['ymin']:
            returnjson['ymin'] = int(onecity['ymin'])
    for onecity in filecontent['municipalities']:
        if int(onecity['xmax']) > returnjson['xmax']:
            returnjson['xmax'] = int(onecity['xmax'])
        if int(onecity['xmin']) < returnjson['xmin']:
            returnjson['xmin'] = int(onecity['xmin'])
        if int(onecity['ymax']) > returnjson['ymax']:
            returnjson['ymax'] = int(onecity['ymax'])
        if int(onecity['ymin']) < returnjson['ymin']:
            returnjson['ymin'] = int(onecity['ymin'])
    for onecity in filecontent['provinces']:
        if int(onecity['xmax']) > returnjson['xmax']:
            returnjson['xmax'] = int(onecity['xmax'])
        if int(onecity['xmin']) < returnjson['xmin']:
            returnjson['xmin'] = int(onecity['xmin'])
        if int(onecity['ymax']) > returnjson['ymax']:
            returnjson['ymax'] = int(onecity['ymax'])
        if int(onecity['ymin']) < returnjson['ymin']:
            returnjson['ymin'] = int(onecity['ymin'])
    with open(allscopeurl,'w') as allscopefile:
        allscopefile.write(json.dumps(returnjson,ensure_ascii=False))
    return HttpResponse('ok')
@csrf_exempt
def getgeo(request):
    return render_to_response('getgeo.html',{'returnstr':request.GET.get('returnstr','')})
@csrf_exempt
def insertdata(request):
    returnstr=request.META.get('HTTP_RETURNSTR')
    insertlist=[]
    for onedata in returnstr.split('|'):
        if onedata != '':
            datasplit=onedata.split(',')
            onepoint=Point(status=datasplit[5],lng=datasplit[2],lat=datasplit[3],tilex=datasplit[0],tiley=datasplit[1],timestamp=datasplit[4])
            insertlist.append(onepoint)
    if len(insertlist) > 0:
        Point.objects.bulk_create(insertlist)
    return HttpResponse(1)
@csrf_exempt
def yngetgeo(request):
    return render_to_response('getgeoyn.html',{'returnstr':request.GET.get('returnstr','')})
@csrf_exempt
def yninsertdata(request):
    returnstr=request.META.get('HTTP_RETURNSTR')
    insertlist=[]
    for onedata in returnstr.split('|'):
        if onedata != '':
            datasplit=onedata.split(',')
            onepoint=Point(status=datasplit[5],lng=datasplit[2],lat=datasplit[3],tilex=datasplit[0],tiley=datasplit[1],timestamp=datasplit[4])
            insertlist.append(onepoint)
    if len(insertlist) > 0:
        ynPoint.objects.bulk_create(insertlist)
    return HttpResponse(1)
