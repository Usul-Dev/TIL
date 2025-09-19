"""
https://www.acmicpc.net/problem/24267
"""

import sys
input_data = int(sys.stdin.readline().strip())
print(input_data*(input_data-1)*(input_data-2)//6)
print(3)