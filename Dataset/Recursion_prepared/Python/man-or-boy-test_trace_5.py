#!/usr/bin/env python
import sys
sys.setrecursionlimit(1025)

def a(in_k, x1, x2, x3, x4, x5):
    k = [in_k]
    def b():
        k[0] -= 1
        return a(k[0], b, x1, x2, x3, x4)
    return x4() + x5() if k[0] <= 0 else b()

x = lambda i: lambda: i
print(a(0, x(10), x(9), x(8), x(7), x(6)))