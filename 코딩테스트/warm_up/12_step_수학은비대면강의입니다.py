"""
https://www.acmicpc.net/problem/19532
"""

import sys

"""
ax + by = c
dx + ey = f

a b  c d e f
1 3 -1 4 1 7

[1 3][x][-1]
[4 1][y][7]
"""
a,b,c,d,e,f = map(int, sys.stdin.readline().split())
# 크래머의 공식
D = a*e - b*d
x = (c*e - b*f) // D
y = (a*f - c*d) // D

print(x, y)