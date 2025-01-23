def cycpattern_check(a, b):
    if len(b) > len(a):
        return False
    for i in range(len(b)):
        if b in a or b[i:] + b[:i] in a:
            return True
    return False