"""
https://www.acmicpc.net/problem/10988
"""

import sys

data = sys.stdin.readline().strip()

print(int(data == data[::-1]))