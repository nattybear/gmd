# -*- coding: utf-8 -*-

from sys import argv
from binascii import hexlify
from os.path import getsize

# 분석 대상 파일을 인자로 받기
FILENAME = argv[1]

# 파일 열기
fp = open(FILENAME, 'rb')

# 오프셋과 이름을 인자로 받아서 내용 출력
def bin2hex(offset,length, name):
  fp.seek(int(offset, 16))
  value = fp.read(length)
  value = byteswap(value)
  value = hexlify(value)
  dec = int(value, 16)
  print "0x%s(%s): 0x%s(%d)" % (offset, name, value, dec)
  return dec

# 오프셋과 읽어들일 바이트 크기와 이름을 인자로 받아서 문자열 출력
def bin2str(offset, length, name):
  fp.seek(int(offset, 16))
  value = fp.read(length)
  print "0x%s(%s): %s" % (offset, name, value)

# 바이트 오더를 변경하는 함수 정의
def byteswap(string):
  result = ''
  while string != '':
    result += string[-1:]
    string = string[:-1]
  return result

bin2str('0', 3, '파일 헤더')
bin2hex('C', 1, '내부 파일 개수')
bin2hex('10', 1, '텍스트 개수')
bin2hex('14', 1, '전체 내부 파일 이름 길이')
tsize = bin2hex('18', 4, '전체 텍스트 크기')
fnamelen = bin2hex('1C', 1, '파일 이름 길이')
bin2str('20', fnamelen, '파일 이름')

# 파일 크기 구하기
fsize = getsize(FILENAME)

print '파일 크기 : %d byte' % fsize

# 텍스트 시작 위치 구하기
tstart = fsize - tsize
print '텍스트 시작 위치 : %s' % hex(tstart)

# 텍스트 값 읽기
fp.seek(tstart)
text = fp.read(tsize)
text = text.split(b'\x00')

# 텍스트 값 출력하기
for i in text:
  print i
  print

# 추출할 파일 이름 만들기
TEXT_FILE = FILENAME.split('.')[0] + '.txt'

# 텍스트를 파일로 추출하기
fp2 = open(TEXT_FILE, 'wb')
for i in text:
  fp2.write(i)
  fp2.write('\r\n\r\n')

# 파일 닫기
fp.close()
fp2.close()
