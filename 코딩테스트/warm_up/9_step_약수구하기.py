"""
https://www.acmicpc.net/problem/2501
"""

import sys

N, K = map(int, sys.stdin.readline().split())

result = []
for i in range(1, N+1):
    if K == len(result):
        break
    if N % i == 0:
        result.append(i)
try:
    print(result[K-1])
except IndexError:
    print(0)
