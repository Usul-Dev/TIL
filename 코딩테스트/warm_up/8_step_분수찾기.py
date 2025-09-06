"""
https://www.acmicpc.net/problem/1193
"""


import sys

input_number = int(sys.stdin.readline())
line = 1

while input_number > line:
    input_number -= line
    line += 1

if line%2 ==0:
    print(f"{input_number}/{line-input_number+1}")
else:
    print(f"{line-input_number+1}/{input_number}")
