"""
https://www.acmicpc.net/problem/9086
"""

import sys
for _ in range(int(sys.stdin.readline())):
    str_data = str(sys.stdin.readline().strip())
    print(str_data[0] + str_data[-1])

