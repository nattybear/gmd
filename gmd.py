# -*-coding: utf-8 -*-

from binascii import hexlify
from os.path import getsize
from sys import argv

FILENAME = argv[1]

# 파일 열기
fp = open(FILENAME, 'rb')

# 파일 헤더 구하기
header = fp.read(3)

# 파일 헤더가 GMD가 아니면 프로그램 종료
if header != 'GMD':
  print 'Header is Not GMD'
  exit()

# 0xC 값 구하기
fp.seek(int('c', 16))
count = int(hexlify(fp.read(1)), 16)

# 0xC 값이 01이 아니면 프로그램 종료
if count != 1:
  print '0xC is not 1'
  exit()

# 0x18 값 구하기
fp.seek(int('18', 16))
textlen = int(hexlify(fp.read(1)), 16)

# 파일 크기 구하기
size = getsize(FILENAME)

# 텍스트 위치로 이동
fp.seek(size - textlen)

# 텍스트 위치에서 텍스트 크기만큼 읽기
text = fp.read(textlen)

# 텍스트 0x00으로 구분하기
text = text.split(b'\x00')

# 텍스트 추출 파일 이름 만들기
NEW = FILENAME.split('.')[0] + '.txt'

# 새 파일 열기
fp2 = open(NEW, 'wb')

# 추출한 텍스트 새 파일에 쓰기
for i in text:
  fp2.write(i)
  fp2.write('\n')

# 파일 닫기
fp.close()
fp2.close()
