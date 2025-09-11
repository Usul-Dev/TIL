"""
https://www.acmicpc.net/problem/2581
"""

import sys
from math import sqrt
N = int(sys.stdin.readline().strip())
M = int(sys.stdin.readline().strip())

result = []

def is_prime_number(n):
    if n < 2:
        return False
    for i in range(2, int(sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

for i in range(N, M + 1):
    if is_prime_number(i):
        result.append(i)

if len(result) > 0:
    print(sum(result))
    print(min(result))
else:
    print(-1)