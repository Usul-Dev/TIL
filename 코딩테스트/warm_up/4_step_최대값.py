"""
https://www.acmicpc.net/problem/2562
"""

import sys

result = {}
for i in range(1, 10):
    a = int(sys.stdin.readline())
    result[a] = i

k = max(result)
print(k)
print(result[k])