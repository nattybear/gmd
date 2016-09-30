# -*- coding: utf-8 -*-

from csv import reader
from sys import argv

# 테이블 파일 읽기
table_handle = open('Korean.tbl', 'rb')

# 테이블 파일 csv로 읽기
csvfile = reader(table_handle, delimiter='=')

# 분석 대상 파일 열기
fp = open(argv[1], 'rb')

# 분석 대상 파일 내용 읽기
buf = fp.read()

# 분석 대상 파일 내용 테이블에 따라 치환하기
for i in csvfile:
  buf = buf.replace(i[1], i[0])

print buf
