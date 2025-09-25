"""
https://www.acmicpc.net/problem/2231
"""

import sys
N = int(sys.stdin.readline().strip())

result = 0
start = max(1, N - 9 * len(str(N)))

for M in range(start, N):
    if M + sum(map(int, str(M))) == N:
        result = M
        break
print(result)