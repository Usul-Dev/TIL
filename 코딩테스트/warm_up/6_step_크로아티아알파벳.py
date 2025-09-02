"""
https://www.acmicpc.net/problem/2941
"""
import sys

data = sys.stdin.readline().strip()
replace_data = ["c=", "c-", "dz=", "d-", "lj", "nj", "s=", "z="]
count = 0
for i in replace_data:
    data = data.replace(i, "@")

print(len(data))

