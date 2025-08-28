"""
https://www.acmicpc.net/problem/2675
"""

import sys

result = []
for i in range(int(sys.stdin.readline().strip())):
    R, S = sys.stdin.readline().split()
    for string_data in S:
        result.append(string_data*int(R))

    print(''.join(result))
    result = []


