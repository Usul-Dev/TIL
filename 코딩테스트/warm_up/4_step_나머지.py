"""
https://www.acmicpc.net/problem/3052
"""

import sys
result = set()
for _ in range(10):
    result.add(int(sys.stdin.readline()) % 42)
print(len(result))