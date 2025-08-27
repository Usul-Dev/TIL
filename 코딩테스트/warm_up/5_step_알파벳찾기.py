"""
https://www.acmicpc.net/problem/10809
"""

import sys

data = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t","u", "v", "w", "x", "y", "z"]
data_dict = {i: -1 for i in data}

for i, v in enumerate(sys.stdin.readline().strip()):
    if data_dict[v] == -1:data_dict[v] = i
print(*data_dict.values())