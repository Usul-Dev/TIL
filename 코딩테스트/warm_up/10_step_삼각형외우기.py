"""
https://www.acmicpc.net/problem/10101
"""

import sys
result = []
for _ in range(3):
    result.append(int(sys.stdin.readline().strip()))

if result.count(60) == 3:
    print("Equilateral")
elif sum(result) == 180:
    result.sort()
    if result[0] == result[1] or result[1] == result[2]:
        print("Isosceles")
    else:
        print("Scalene")
else:
    print("Error")