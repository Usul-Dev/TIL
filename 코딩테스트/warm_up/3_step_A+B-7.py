"""
https://www.acmicpc.net/problem/11021
"""
import sys

for i in range(int(sys.stdin.readline())):
    a, b = map(int, sys.stdin.readline().split())
    print(f"Case #{i+1}: {a+b}")



