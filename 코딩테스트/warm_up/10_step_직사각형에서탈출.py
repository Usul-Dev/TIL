"""
https://www.acmicpc.net/problem/1085
"""
import sys

x,y,w,h = map(int, sys.stdin.readline().split())
print(min([(w-x),(h-y), (x-0), (y-0)]))