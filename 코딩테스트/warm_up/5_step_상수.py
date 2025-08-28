"""
https://www.acmicpc.net/problem/2908
"""

import sys
A, B = sys.stdin.readline().split()
print(max(A[::-1], B[::-1]))