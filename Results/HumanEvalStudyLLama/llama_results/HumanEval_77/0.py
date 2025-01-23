import math

def iscube(a):
    root = round(abs(a) ** (1./3))
    return root ** 3 == abs(a)