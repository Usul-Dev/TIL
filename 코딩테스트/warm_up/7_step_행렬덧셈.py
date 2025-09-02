"""
https://www.acmicpc.net/step/2
"""

import sys

N, M = map(int, sys.stdin.readline().split())
A = [list(map(int, sys.stdin.readline().split())) for _ in range(N)]
B = [list(map(int, sys.stdin.readline().split())) for _ in range(N)]
for i in range(N):
    result = []
    for j in range(M):
        result.append(A[i][j] + B[i][j])
    print(*result)
