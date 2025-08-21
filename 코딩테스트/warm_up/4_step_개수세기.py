"""
https://www.acmicpc.net/problem/10807
"""

import sys

_ = sys.stdin.readline().strip()
num_list = sys.stdin.readline().split()
find_num = sys.stdin.readline().strip()

print(num_list.count(find_num))