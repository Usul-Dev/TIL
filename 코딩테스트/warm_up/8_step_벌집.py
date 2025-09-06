"""
https://www.acmicpc.net/problem/2292
"""


import sys

input_data = int(sys.stdin.readline().strip())
number = 1
for i in range(input_data):
    number += i * 6
    if input_data <= number:
        print(i+1)
        break