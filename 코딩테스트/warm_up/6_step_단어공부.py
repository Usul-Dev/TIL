"""
https://www.acmicpc.net/problem/1157
"""

import sys

data = sys.stdin.readline().strip()

result = dict()
new_result = []
for i in data:
    if not result.get(i.upper()):
        result[i.upper()] = 1
    else:
        result[i.upper()] += 1

max_data = max(result.values())
for k, v in result.items():
    if v == max_data:
        new_result.append(k)

print("?" if len(new_result) > 1 else new_result[0])
