# _*_ coding:utf-8 _*_
from django.shortcuts import render
import datetime
import json
from django.http import HttpResponse
from PySE.spider import news_downloader
from PySE.process_text import TextProcesser
# Create your views here.

def grab_web(request):
    content = {}
    if 'c' in request.GET:
        c = request.GET['c']
        dl = news_downloader(pages=2)
        dl.start(c)
        content['res'] = 'OK'
    else:
        content['res'] = 'ERROR'
    return HttpResponse(json.dumps(content), content_type="application/json")

def handle(request):
    content = {}
    cls = TextProcesser()
    tm = cls.start()
    if tm > 0:
        content['res'] = 'OK'
        content['tm'] = tm
    else:
        content['res'] = 'ERROR'
    return HttpResponse(json.dumps(content), content_type="application/json")