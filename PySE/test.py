# _*_ coding:utf-8 _*_
import chardet
from PySE.process_text import word_segment
__author__ = 'T'

s = '护渔  水面'

l = list(word_segment(s))
for x in l:
    print(x)



