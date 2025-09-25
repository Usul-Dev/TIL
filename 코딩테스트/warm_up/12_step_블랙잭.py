"""
https://www.acmicpc.net/problem/2798
"""
"""
5 21
5 6 7 8 9

1. 5 6
2. 5 7
3. 5 8
4. 5 9
---
1. 6 7
2. 6 8
3. 6 9
---
1. 7 8
2. 7 9
---
1. 8 9

"""
import sys
N, M = map(int, sys.stdin.readline().split())
cards = list(map(int, sys.stdin.readline().split()))

best = 0
for i in range(N):
    for j in range(i + 1, N):
        for k in range(j + 1, N):
            s = cards[i] + cards[j] + cards[k]
            if M >= s > best:
                best = s

print(best)