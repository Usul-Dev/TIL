"""
https://www.acmicpc.net/problem/11005

10진수를 다른 진법으로 변환할떈 나누기
"""

import sys

N, B = map(int, sys.stdin.readline().split())

digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
result = []

while N > 0:
    N, r = divmod(N, B)
    result.append(digits[r])

print("".join(reversed(result)))
