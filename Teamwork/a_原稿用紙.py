# https://atcoder.jp/contests/pakencamp-2019-day4/tasks/pakencamp_2019_day4_a
import sys
sys.setrecursionlimit(2147483647)
INF=float("inf")
MOD=10**9+7 # 998244353
input=lambda:sys.stdin.readline().rstrip()
def resolve():
    n=int(input())
    print((n-1)//400+1)
resolve()
