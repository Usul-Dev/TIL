"""
https://www.acmicpc.net/problem/24313
"""

import sys

a1, a0 = map(int, sys.stdin.readline().split())
c = int(sys.stdin.readline())
n = int(sys.stdin.readline())

if a1 > c:
    print(0)
elif a1 == c:
    print(1 if a0 <= 0 else 0)
else:
    print(1 if (a1-c) * n + a0 <= 0 else 0)