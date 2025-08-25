"""
https://www.acmicpc.net/problem/1546
"""

import sys
N = int(sys.stdin.readline().strip())

data = list(map(int, sys.stdin.readline().split()))
max_data = max(data)
number_list = []
for i in data:
    number_list.append(int(i)/int(max_data)*100)
print(round(sum(number_list)/len(data), 6))

