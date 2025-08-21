"""
https://www.acmicpc.net/problem/10951
"""

import sys

while True:
    try:
        a, b = map(int, sys.stdin.readline().split())
    except ValueError:
        break
    print(a + b)
