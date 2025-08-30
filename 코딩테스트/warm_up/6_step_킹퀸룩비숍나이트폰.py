"""
https://www.acmicpc.net/problem/3003
"""

import sys

need = [1, 1, 2, 2, 2, 8]
have = list(map(int, sys.stdin.readline().split()))
res = [a - b for a, b in zip(need, have)]
print(*res)