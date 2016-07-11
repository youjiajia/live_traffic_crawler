# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Point(models.Model):
    tilex=models.CharField(max_length=50, verbose_name='瓦片横坐标')
    tiley=models.CharField(max_length=50, verbose_name='瓦片纵坐标')
    lat=models.CharField(max_length=50, verbose_name='纬度')
    lng=models.CharField(max_length=50, verbose_name='经度')
    timestamp=models.CharField(max_length=50, verbose_name='时间戳')
    status=models.CharField(max_length=50, default='1')
class ynPoint(models.Model):
    tilex=models.CharField(max_length=50, verbose_name='瓦片横坐标')
    tiley=models.CharField(max_length=50, verbose_name='瓦片纵坐标')
    lat=models.CharField(max_length=50, verbose_name='纬度')
    lng=models.CharField(max_length=50, verbose_name='经度')
    timestamp=models.CharField(max_length=50, verbose_name='时间戳')
    status=models.CharField(max_length=50, default='1')
