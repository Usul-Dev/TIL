"""
https://www.acmicpc.net/problem/1978
"""

import sys
from math import sqrt

N = int(sys.stdin.readline().strip())
numbers = list(map(int, sys.stdin.readline().strip().split()))

def is_prime_number(n):
    if n < 2:
        return False
    for i in range(2, int(sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

count = 0
for num in numbers:
    if is_prime_number(num):
        count += 1

print(count)