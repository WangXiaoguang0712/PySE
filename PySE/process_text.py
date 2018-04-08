# _*_coding:utf-8 _*_
import jieba
import re
import os
import time
import numpy as np
from PySE.DBHelper import DBHelper
__author__ = 'T'


def fn_time(fn):
    def _wrapper(*args, **kwargs):
        start = time.clock()
        res = fn(*args, **kwargs)
        tm = time.clock() - start
        return res, tm
    return _wrapper


def remove_noise(text):
    pattern = re.compile(r'　　|\t{2,}|\r|\n| 	|\d{1,}.?|[“•”。！，：（）、；/]|[a-z]|[A-Z]', re.S)
    text = re.sub(pattern, ' ', text)
    return  text


def word_segment(text):
    # 读取停用词
    sw_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/stopwords.txt')
    with open(sw_file, 'rb') as fr:
        l_stopwords = [line for line in fr.readlines()]
    for w in jieba.cut(text):
        if w.encode('utf-8') not in l_stopwords and w != ' ':
            yield w

class TextProcesser():
    def __init__(self):
        pass

    @fn_time
    def process_text(self, idx_max_rowid):
        db = DBHelper()
        # 最大rowid
        idx_batch_max = idx_max_rowid
        tmp = db.select("select max(rowid) from news;")[0][0]
        if tmp is not None:
            idx_batch_max = tmp
        # 所有文章
        l_all_content = db.select("select rowid,news_content from news;")
        d_all_content = dict(l_all_content)
        # 所有已索引的词
        l_all_words = db.select("select word from news_idx;")
        l_all_words = [x[0] for x in l_all_words]
        # 需要索引的文章
        l_content = db.select("select rowid,news_content from news where rowid>"+ str(idx_max_rowid))
        s_batch_words = set()
        d_batch_words_idx_insert = {}
        d_batch_words_idx_update = {}
        for key, val in l_content:
            l_current_words = list(word_segment(remove_noise(val)))
            # 计算tf 值
            d_word_tf = { x : l_current_words.count(x) / len(l_current_words) for x in l_current_words }
            sql_inner = ""
            for key_inner, val_inner in d_word_tf.items():
                sql_inner += "('" + str(key_inner) + "','" + str(key) + "'," + str(val_inner) + "),"
            sql = "insert into words_tf values" + sql_inner.rstrip(',')
            db.exec_sql(sql)

            s_current_words = set(l_current_words)
            s_sub_words = s_current_words - s_batch_words
            s_batch_words = s_batch_words | s_sub_words
            for w in s_sub_words:
                l_idx = []
                if w in l_all_words:
                    l_idx = [x[0] for x in filter(lambda x: x[1].count(w) > 0 and x[0] > idx_max_rowid , d_all_content.items())]
                    d_batch_words_idx_update[w] = str(l_idx).lstrip('[').rstrip(']')
                else:
                    l_idx = [x[0] for x in filter(lambda x: x[1].count(w) > 0, d_all_content.items())]
                    d_batch_words_idx_insert[w] = str(l_idx).lstrip('[').rstrip(']')
        # 插入
        print('sql begin')
        if len(d_batch_words_idx_insert.keys()) > 0:
            sqlinner = ""
            for key, val in d_batch_words_idx_insert.items():
                sqlinner += "('" + key + "','" + val + "'),"
            sql = "insert into news_idx values" + sqlinner.rstrip(',')
            print(sql)
            db.exec_sql(sql)
        # 更新
        if len(d_batch_words_idx_update.keys()) > 0:
            db.exec_sql("delete from news_idx_tmp;")
            sqlinner = ""
            for key, val in d_batch_words_idx_update.items():
                sqlinner += "('" + key + "','" + val + "'),"
            sql = "insert into news_idx_tmp values" + sqlinner.rstrip(',')
            print(sql)
            db.exec_sql(sql)
            #  需要数据库唯一索引
            sql = "replace into news_idx " \
                  "select b.word,a.idx ||','||b.idx from news_idx a inner join news_idx_tmp b on a.word=b.word"
            print(sql)
            db.exec_sql(sql)

        #  计算idf 值
        # 删掉历史idf
        sql = "delete from words_idf;"
        db.exec_sql(sql)
        # 总文档数
        sql = "select count(*) from news;"
        i_doc = db.select(sql)[0][0]

        # 特定词的文档数
        sql = "select word,idx from news_idx;"
        l_word_idx = db.select(sql)
        s_idf = {}
        sql_inner = ""
        for x in l_word_idx:
            tmp_idf =  np.log(i_doc / len(x[1].split(',')))
            sql_inner += "('" + str(x[0]) + "'," + str(tmp_idf) + "),"
        sql = "insert into words_idf values" + sql_inner.rstrip(',')
        db.exec_sql(sql)
        return idx_batch_max

    def start(self):
        db = DBHelper()
        #  查询已处理最大rowid
        idx_max_rowid = 0
        idx_max = db.select("select max(rowid_max) from news_idx_max;")[0][0]
        if idx_max is not None:
            idx_max_rowid = idx_max
        res, tm = self.process_text(idx_max_rowid)
        print(tm)
        #  更新处理记录
        db.exec_sql("insert into  news_idx_max select "+ str(res) +",CURRENT_TIMESTAMP,"+str(tm)+" ;")
        return tm

if __name__ == "__main__":
    cls = TextProcesser()
    cls.start()

