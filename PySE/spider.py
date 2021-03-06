# _*_ coding:utf-8 _*_

from urllib import request
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import sqlite3
import json
import chardet
import re
from PySE.DBHelper import DBHelper

__author__ = 'T'


class news_downloader():
    def __init__(self, pages=1):
        self.size = 10
        self.pages = pages
        self.db = ''

    def get_html(self, url):
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                     'Chrome/62.0.3202.94 Safari/537.36'
        header = {'User-Agent': user_agent}
        req = request.Request(url, headers=header)
        try:
            web = request.urlopen(req).read()#.decode('gbk','ignore')
            # print(web)
            # BeautifulSoup(web, 'html.parser')
            return web
        except:
            print('open weburl error')
            return None

    def download(self, class_id, url):
        self.db = DBHelper()
        if class_id == 0:  # 军事
            for page in range(1, self.pages + 1):
                url = url + '&page=' + str(page)+'&show_num='+ str(self.size)
                web = self.get_html(url)
                #print(web)
                dict_web = eval(web)
                for item in dict_web["result"]['data']:
                    news_title = item['title']
                    news_addr = re.sub(r'\\', '', item['url'])
                    sql = "select count(*) from news where news_addr='"+news_addr+"'"
                    if self.db.select(sql)[0][0] == 0:
                        soup = BeautifulSoup(self.get_html(news_addr), 'html.parser')
                        news_content = soup.find('div', attrs={'id': 'article'}).get_text()
                        pat = re.compile(r'(SinaPage.+\}\);)|\n{2,}', re.S)
                        news_content = re.sub(pat, '', news_content)
                        print(news_addr)
                        sql = "insert into news values('"+str(class_id)+"','"+news_addr+"','"+news_title+"','"+news_content+"')"
                        self.db.exec_sql(sql)
        elif class_id == 1:
            for page in range(1, self.pages + 1):
                url_temp = url + '&num='+ str(self.size) +'&page=' + str(page)
                print(url_temp)
                web = self.get_html(url_temp)
                dict_web = eval(web)
                for item in dict_web["result"]['data']:
                    news_addr = re.sub('\\\\', '', item['wapurl'])
                    news_title = item['title']
                    sql = "select count(*) from news where news_addr='"+news_addr+"'"
                    if self.db.select(sql)[0][0] == 0:
                        soup = BeautifulSoup(self.get_html(news_addr), 'html.parser')
                        news_content = soup.find('article', attrs={'class': 'art_box'}).get_text()
                        pat1 = re.compile(r'\n{2,}', re.S)
                        pat2 = re.compile(r'\t{6,}.+\t{5,}|window.STO.+getTime\(\)\;')
                        news_content = re.sub(pat2, '', re.sub(pat1, '\n', news_content))
                        # print(news_content.encode('gbk', 'ignore'))
                        sql = "insert into news values('"+str(class_id)+"','"+news_addr+"','"+news_title+"','"+news_content+"')"
                        self.db.exec_sql(sql)
        elif class_id == 2:
            for page in range(1, self.pages + 1):
                url_temp = url + '&size='+ str(self.size) +'&page=' + str(page)
                print(url_temp)
                web = self.get_html(url_temp)
                dict_web = eval(web)
                for item in dict_web["result"]['data']['articles']:
                    news_addr = re.sub('\\\\', '', item['pub_url'])
                    news_title = item['title']
                    sql = "select count(*) from news where news_addr='"+news_addr+"'"
                    if self.db.select(sql)[0][0] == 0:
                        soup = BeautifulSoup(self.get_html(news_addr), 'html.parser')
                        news_content = soup.find('div', attrs={'id': 'artibody'}).get_text()
                        pat1 = re.compile(r'\n{2,}', re.S)
                        pat2 = re.compile(r'\t{6,}.+\t{5,}|window.STO.+getTime\(\)\;')
                        news_content = re.sub(pat2, '', re.sub(pat1, '\n', news_content))
                        # print(news_content.encode('gbk', 'ignore'))
                        sql = "insert into news values('"+str(class_id)+"','"+news_addr+"','"+news_title+"','"+news_content+"')"
                        self.db.exec_sql(sql)

        elif class_id == 3:
            for page in range(1, self.pages + 1):
                url_temp = url + '&size='+ str(self.size) +'&page=' + str(page)
                print(url_temp)
                web = self.get_html(url_temp)
                dict_web = eval(web)
                for item in dict_web["result"]['data']:
                    news_title = item['title']
                    news_addr = re.sub(r'\\', '', item['url'])
                    sql = "select count(*) from news where news_addr='"+news_addr+"'"
                    if self.db.select(sql)[0][0] == 0:
                        soup = BeautifulSoup(self.get_html(news_addr), 'html.parser')
                        news_content = soup.find('div', attrs={'class': 'article'}).get_text()
                        pat = re.compile(r'(SINA_TEXT_PAGE_INFO.+\}\]\;)|(SinaPage.+\}\);)|\n{2,}', re.S)
                        news_content = re.sub(pat, '', news_content)
                        #print(news_content)
                        sql = "insert into news values('"+str(class_id)+"','"+news_addr+"','"+news_title+"','"+news_content+"')"
                        self.db.exec_sql(sql)
        elif class_id == 4:
            for page in range(1, self.pages + 1):
                url_temp = url + '&show_num='+ str(self.size) +'&page=' + str(page)
                print(url_temp)
                web = self.get_html(url_temp)
                dict_web = eval(web)
                for item in dict_web["result"]['data']:
                    news_title = item['title']
                    news_addr = re.sub(r'\\', '', item['url'])
                    sql = "select count(*) from news where news_addr='"+news_addr+"'"
                    if self.db.select(sql)[0][0] == 0:
                        soup = BeautifulSoup(self.get_html(news_addr), 'html.parser')
                        news_content = soup.find('div', attrs={'id': 'artibody'}).get_text()
                        pat = re.compile(r'(SINA_TEXT_PAGE_INFO.+\}\]\;)|(SinaPage.+\}\);)|\n{2,}', re.S)
                        news_content = re.sub(pat, '', news_content)
                        # print(news_content.encode('gbk', 'ignore'))
                        sql = "insert into news values('"+str(class_id)+"','"+news_addr+"','"+news_title+"','"+news_content+"')"
                        self.db.exec_sql(sql)

        elif class_id == 5:
            for page in range(1, self.pages + 1):
                url_temp = url + '?page=' + str(page)
                print(url_temp)
                soup = BeautifulSoup(self.get_html(url_temp), 'html.parser')
                l_news = soup.find_all('div', attrs={"class":"con"})
                for news in l_news:
                    res = news.find('h3')
                    news_title = res.text
                    news_addr = res.a.get('href')
                    sql = "select count(*) from news where news_addr='"+news_addr+"'"
                    if self.db.select(sql)[0][0] == 0:
                        soup = BeautifulSoup(self.get_html(news_addr), 'html.parser')
                        news_content = soup.find('div', attrs={'id': 'artibody'})#.get_text()
                        pat3 = re.compile(r'<script.*?>.*?</script>|<.+?>', re.S)
                        news_content = re.sub(pat3, '', str(news_content))

                        pat1 = re.compile(r'\n{2,}', re.S)
                        news_content = re.sub(pat1, '\n', news_content)
                        # print(chardet.detect(news_content))
                        # print(news_content.decode('utf-8').encode('gbk', 'ignore'))
                        sql = "insert into news values('" + str(class_id) + "','" + news_addr + "','" + news_title + "','" + news_content + "')"
                        self.db.exec_sql(sql)
        else:
            pass


    def start(self, col=''):
        db = DBHelper()
        sql = ""
        if col == '':
            sql = "select * from news_class"
        else:
            sql = "select * from news_class where id='" + str(col) + "'"
        res = db.select(sql)
        for item in res:
            #print(item[2])
            self.download(item[0], item[2])

if __name__ == '__main__':
    dl = news_downloader(pages=1)
    dl.start(1)
