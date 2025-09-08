"""
https://www.acmicpc.net/step/10
"""

import sys

while True:
    a, b = map(int, sys.stdin.readline().split())
    if not all([a, b]):
        break

    if a % b == 0:
        print("multiple")
    elif b % a == 0:
        print("factor")
    else:
        print("neither")
