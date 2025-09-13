"""
https://www.acmicpc.net/problem/3009
"""

import sys

x_result = 0
y_result = 0
for _ in range(3):
    x, y = map(int, sys.stdin.readline().split())
    x_result ^= x
    y_result ^= y

print(x_result, y_result)

