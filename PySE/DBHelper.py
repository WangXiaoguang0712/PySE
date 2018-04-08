import sqlite3
import os
__author__ = 'T'


class DBHelper(object):
    def __init__(self):
        db_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_name = os.path.join(db_path, 'news.db')
        self.db_name = db_name

    def exec_sql(self, sql):
        if len(sql) == 0:
            raise ValueError('parameter can not be null')
        else:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            # print(sql)
            cursor.execute(sql)
            # print(cursor.rowcount)
            conn.commit()
            conn.close()

    def select(self, sql):
        if len(sql) == 0:
            raise ValueError('parameter can not be null')
        else:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            result = cursor.execute(sql)
            result = list(result)
            cursor.close()
            conn.close()
            return result
