"""
https://www.acmicpc.net/problem/5597
"""
import sys

data = [0] * 30

for _ in range(28):
    출석번호 = int(sys.stdin.readline().rstrip())
    data[출석번호-1] = 출석번호
print(data.index(min(data))+1)
data.remove(min(data))
print(data.index(min(data))+2)