# -*- coding: utf-8 -*-

from sys import argv
from struct import pack, unpack
from os.path import getsize
from csv import reader

ORIGIN = argv[1]
PATCH = argv[2]
NEW = ORIGIN.split('.')[0] + '_patch.gmd'

# 패치 파일 열기
fp = open(PATCH, 'rb')

# patch 변수 초기화
patch = ''

# csv 객체 만들기
c = reader(fp)

# csv 파일에서 번역만 읽어서 patch 변수에 저장하기
for i in c:
  patch += i[1] + b'\x00'

# patch에서 마지막 1바이트 빼기
patch = patch[:-1]

# 패치 크기 구하기
psize = len(patch)

# 원본 파일 열기
fp2 = open(ORIGIN, 'rb')

# 패치 적용 파일 만들기
fp3 = open(NEW, 'wb')

# 파일 크기 구하기
fsize = getsize(ORIGIN)

# 텍스트 전체 길이 구하기
fp2.seek(int('18', 16))
tsize = fp2.read(4)
tsize = unpack('I', tsize)[0]

# 텍스트 시작 위치 구하기
tstart = fsize - tsize

# 패치 적용 파일에 원본 파일 쓰기
fp2.seek(0)
fp3.write(fp2.read(tstart - 1))

# 패치 크기 가공하기
psize = pack('I', psize)

# 패치 적용 파일에 텍스트 크기 수정하기
fp3.seek(int('18', 16))
fp3.write(psize)

# 패치 파일 쓰기
fp3.seek(tstart)
fp3.write(patch)

# 파일 닫기
fp.close()
fp2.close()
fp3.close()
