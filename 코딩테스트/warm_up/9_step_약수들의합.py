"""
https://www.acmicpc.net/problem/9506
"""

import sys

while True:
    N = int(sys.stdin.readline().strip())
    if N == -1:
        break

    divs = [i for i in range(1, N) if N % i == 0]
    if sum(divs) == N:
        print(f"{N} = " + " + ".join(map(str, divs)))
    else:
        print(f"{N} is NOT perfect.")