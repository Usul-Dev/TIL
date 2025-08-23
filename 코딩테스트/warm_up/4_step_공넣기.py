"""
https://www.acmicpc.net/problem/10810

-     1,   2,   3,   4,   5
[1]  3[X] 3[X]
[2]            4[X] 4[X]
[3]  1    1    1    1
[4]       2
===========================
=>   1    2    1    1    0
"""

import sys

N, M = map(int, sys.stdin.readline().split())
n_dict = {i: 0 for i in range(1, N+1)}

for _ in range(M):
    i, j, 공번호 = map(int, sys.stdin.readline().split())
    for v in range(i, j+1):
        if n_dict[v] > 0:
            if n_dict[v]+1 == 공번호: # 순차적체크
                n_dict[v] = 공번호
            elif n_dict[v] != 공번호:
                n_dict[v] = 공번호
        elif n_dict[v] == 0:
            n_dict[v] = 공번호


print(*n_dict.values())