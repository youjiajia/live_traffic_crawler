# -*- coding: utf-8 -*-
from django.conf.urls import url
from road.views import *

urlpatterns = [
    # url(r'^importtiles/$', gettiles, name='importtiles'),
    # url(r'^updatefile/$', updatefile, name='updatefile'),
    # url(r'^getallfile/$', getallfile, name='getallfile'),
    url(r'^getchinascope/$', getchinascope, name='getchinascope'),
    url(r'^insertdata/$', insertdata, name='insertdata'),
    url(r'^getgeo/$', getgeo, name='getgeo'),
    url(r'^yninsertdata/$', yninsertdata, name='yninsertdata'),
    url(r'^yngetgeo/$', yngetgeo, name='yngetgeo'),
]
