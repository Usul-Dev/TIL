"""
https://www.acmicpc.net/problem/10871
"""

import sys

N, X = map(int, sys.stdin.readline().split())
A = sys.stdin.readline().split()
result = []
for i in range(N):
    if X > int(A[i]):
        result.append(int(A[i]))

sort_result = result
a = ''
for i in sort_result:
    a += f"{i} "

print(a)