"""
https://www.acmicpc.net/problem/11720
"""
import sys

N = int(sys.stdin.readline())
data = sys.stdin.readline()
sum_result = 0
for i in range(N):
    sum_result += int(data[i])
print(sum_result)