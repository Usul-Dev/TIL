"""
https://www.acmicpc.net/problem/2869
"""

import sys
A, B, V = map(int, sys.stdin.readline().split())
days = (V - B + (A - B) - 1) // (A - B)
print(days)