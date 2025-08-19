"""
https://www.acmicpc.net/problem/25304
- 영수증
"""
총금액 = int(input())

결과 = 0
for _ in range(int(input())):
    금액, 갯수 = map(int, input().split())
    결과 += 금액 * 갯수

print("Yes" if 총금액 == 결과 else "No")