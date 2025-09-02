"""
https://www.acmicpc.net/problem/2566
"""

import sys
result_dict = {}
for i in range(1, 10):
    result_dict[i] = list(map(int, sys.stdin.readline().split()))

current_max_num = 0
index = '1 1'
for k, v in result_dict.items():
    if max_num:= max(result_dict[k]):
        if current_max_num < max_num:
            current_max_num = max_num
            index = f"{k} {v.index(max_num)+1}"

print(current_max_num)
print(index)