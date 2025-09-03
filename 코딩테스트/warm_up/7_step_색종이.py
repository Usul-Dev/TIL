"""
https://www.acmicpc.net/problem/2563
"""

import sys

n = int(sys.stdin.readline())
paper = [[0]*100 for _ in range(100)]

for _ in range(n):
    x, y = map(int, sys.stdin.readline().split())
    for i in range(x, x+10):
        for j in range(y, y+10):
            paper[i][j] = 1

result = 0
for row in paper:
    result += sum(row)

print(result)
