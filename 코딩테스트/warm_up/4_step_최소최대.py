"""
https://www.acmicpc.net/problem/10818
"""

import sys
_ = sys.stdin.readline()
B = sys.stdin.readline().split()
result = [int(i) for i in B]
print(min(result), max(result))