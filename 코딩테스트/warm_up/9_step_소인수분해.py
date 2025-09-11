"""
https://www.acmicpc.net/problem/11653
"""

import sys

def factorize2(n):
    factor = 2
    while factor**2 <= n:
        while n % factor == 0:
            print(factor)
            n = n // factor
        factor += 1
    if n > 1 :
        print(n)

input_data = int(sys.stdin.readline().strip())
factorize2(input_data)