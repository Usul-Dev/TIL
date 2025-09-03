"""
https://www.acmicpc.net/problem/10798
"""

import sys

result_dict = {}
for i in range(5):
    for k, v in enumerate(sys.stdin.readline().strip()):
        if result_dict.get(k):
            result_dict[k] += v
        else:
            result_dict[k] = v

for k in result_dict.keys():
    print(result_dict[k], end='')
