# _*_ coding:utf-8 _*_
import datetime
import time
import jieba
from django.shortcuts import render
from django.http import HttpResponse
from PySE import DBHelper
from PySE.process_text import word_segment
# Create your views here.


def sayHello(request):
    s = 'Hello World!'
    current_time = datetime.datetime.now()
    html = '<html><head></head><body><h1> %s </h1><p> %s </p></body></html>' % (s, current_time)
    return HttpResponse(html)


def news_index(request):
    context = {}
    context['title'] = '采集地址'
    db =  DBHelper.DBHelper()
    sql = """
    select b.id,b.class_name,count(*)cnt from news a inner join news_class b on a.news_class=b.id
    group by b.id,b.class_name;
    """
    l_news_class = db.select(sql)
    context['list'] = l_news_class
    return render(request, 'index.html', context)


def news_list(request):
    context = {}
    context['title'] = '新闻'
    db =  DBHelper.DBHelper()
    news_class = request.GET['c']
    l_news = db.select("select news_addr,news_title from news where news_class='"+news_class+"';")
    context['news'] = l_news
    return render(request, 'list.html', context)

def news_detail(request):
    context = {}
    db =  DBHelper.DBHelper()
    news_addr = request.GET['addr']

    news = db.select("select news_content,news_title from news where news_addr='" + news_addr + "';")
    context['title'] = news[0][1]
    context['content'] = news[0][0]
    if 'kw' in request.GET:
        kw = request.GET['kw']
        for x in kw.split(','):
            context['content'] = context['content'].replace(x, '<b>' + x + '</b>')
    return render(request, 'detail.html', context)


def news_search(request):
    context = {}
    return render(request, 'search.html', context)


def news_searched(request):
    context = {}
    if request.method == 'POST':
        time_begin = time.clock()
        context['title'] = "查询结果"
        kw = request.POST.get('kw')
        data = list(word_segment(kw))
        sql_inner = ""
        kw = ""
        for w in data:
            sql_inner += " and word='" + str(w) + "'"
            kw += str(w) + ","
        sql = "select idx from news_idx where 1=1" + sql_inner
        db = DBHelper.DBHelper()
        res = db.select(sql)
        if len(res) > 0:
            context['status'] = "OK"
            context['kw'] = kw.rstrip(',')
            sql = """
            select c.rowid,c.news_addr,c.news_title,a.idf*b.tf as tfidf from
            (select idf from words_idf where 1=1 {0} )a cross join (
            select newsid,tf from words_tf where 1=1 {1}  and newsid in({2})
            )b inner join (select rowid,news_addr,news_title from news where rowid in({3}))c on b.newsid=c.rowid
            order by a.idf*b.tf desc
            """.format(sql_inner, sql_inner, str(res[0][0]).replace(' ',''), str(res[0][0]).replace(' ',''))
            # sql = "select news_addr,news_title from news where rowid in()"
            res = db.select(sql)
            context['cnt'] = len(res)
            context['data'] = res
            context['sql'] = sql
        else:
            context['status'] = "WARNING"
            context['data'] = '没有找到您要的文章'
        context['tm'] = time.clock() - time_begin
    else:
        context['status'] = "ERROR"
    return render(request, 'searched.html', context)