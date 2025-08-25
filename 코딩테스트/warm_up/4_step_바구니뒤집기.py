"""
https://www.acmicpc.net/problem/10811
"""

import sys

n, m = map(int, sys.stdin.readline().split())
arr = list(range(1, n + 1))

for _ in range(m):
    i, j = map(int, sys.stdin.readline().split())
    arr[i-1:j] = reversed(arr[i-1:j])
print(*arr)