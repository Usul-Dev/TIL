"""
https://www.acmicpc.net/problem/5073
"""

import sys
while True:
    input_list = list(map(int, sys.stdin.readline().split()))
    input_list.sort()
    if input_list.count(0) == 3: break
    if max(input_list) >= input_list[0] + input_list[1]:
        print("Invalid")
        continue
    if len(set(input_list)) == 1: print("Equilateral")
    elif len(set(input_list)) == 2: print("Isosceles")
    else: print("Scalene")
