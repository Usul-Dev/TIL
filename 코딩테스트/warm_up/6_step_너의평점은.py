"""
https://www.acmicpc.net/problem/25206
"""

import sys

과목평점 = {
    "A+": 4.5,
    "A0": 4.0,
    "B+": 3.5,
    "B0": 3.0,
    "C+": 2.5,
    "C0": 2.0,
    "D+": 1.5,
    "D0": 1.0,
    "F": 0.0,
}
학점누적 = 0
등급누적 = 0
for _ in range(20):
    과목, 학점, 등급 = map(str, sys.stdin.readline().split())
    if 등급 not in "P":
        학점누적 += float(학점)
        등급누적 += float(학점) * 과목평점[등급]

print(등급누적/학점누적)
