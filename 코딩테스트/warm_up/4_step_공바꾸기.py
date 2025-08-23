"""
https://www.acmicpc.net/problem/10813


5 4
1 2
3 4
1 4
2 2

     1  2  3  4  5  [바구니]
[공] 1  2  3  4  5
1>> 2  1  3  4  5
2>> 2  1  4  3  5
3>> 3  1  4  2  5
4>> 3  1  4  2  5
==================
    3  1  4  2  5
"""


import sys

N, M = map(int, sys.stdin.readline().split())
n_dict = {i: i for i in range(1, N+1)}

for _ in range(M):
    i, j = map(int, sys.stdin.readline().split())
    n_dict[i], n_dict[j] = n_dict[j], n_dict[i]

print(*n_dict.values())


