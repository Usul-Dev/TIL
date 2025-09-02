"""
https://www.acmicpc.net/problem/1316
"""
import sys

count = 0

N = int(sys.stdin.readline())

input_data = [sys.stdin.readline().strip() for _ in range(N)]

for i in input_data:
    data_set = set(i)
    result_list = []
    for i, value in enumerate(i):
        if value not in result_list:
            result_list.append(value)
        elif value in result_list:
            if result_list[-1] != value:
                result_list = []
                break
            elif result_list[-1] == value:
                result_list.append(value)
                continue
    if len(data_set) == len(set(result_list)):
        count += 1
print(count)