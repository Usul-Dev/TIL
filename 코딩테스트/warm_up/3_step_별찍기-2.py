"""
https://www.acmicpc.net/problem/2439
"""
import sys
count = int(sys.stdin.readline())
for i in range(1, count+1):
    back_tik = count - i
    print(' '*back_tik + '*'*i)

