"""
https://www.acmicpc.net/problem/9063
"""
import sys
x_list = []
y_list = []

for _ in range(int(sys.stdin.readline().strip())):
    x,y = map(int,sys.stdin.readline().split())
    x_list.append(x)
    y_list.append(y)
print((max(x_list)-min(x_list))*(max(y_list)-min(y_list)))
