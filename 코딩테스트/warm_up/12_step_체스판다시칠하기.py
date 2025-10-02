"""
https://www.acmicpc.net/problem/1018
"""

import sys

N, M = map(int, sys.stdin.readline().split())
board = [sys.stdin.readline().strip() for _ in range(N)]
def repaint_cost(r0, c0, first):
    # first: 'B' 또는 'W' 시작
    flips = 0
    for i in range(8):
        for j in range(8):
            expected = first if (i + j) % 2 == 0 else ('W' if first == 'B' else 'B')
            if board[r0 + i][c0 + j] != expected:
                flips += 1
    return flips

ans = 64  # 최대 8x8 전부 뒤집는 경우
for r in range(N - 7):
    for c in range(M - 7):
        b = repaint_cost(r, c, 'B')
        w = 64 - b  # 보완 관계: W 시작 비용은 64 - B 시작 불일치
        # 또는 w = repaint_cost(r, c, 'W')
        ans = min(ans, b, w)

print(ans)

