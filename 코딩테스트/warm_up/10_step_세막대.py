"""
https://www.acmicpc.net/problem/14215
"""

import sys

a, b, c = sorted(map(int, sys.stdin.readline().split()))
if a + b > c:
    print(a + b + c)
else:
    print(2 * (a + b) - 1)