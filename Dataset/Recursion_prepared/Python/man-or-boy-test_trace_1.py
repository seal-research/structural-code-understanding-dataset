def a(in_k, x1, x2, x3, x4, x5):
    k = [in_k]
    def b():
        k[0] -= 1
        return a(k[0], b, x1, x2, x3, x4)
    return x4() + x5() if k[0] <= 0 else b()

x = lambda i: lambda: i

if __name__ == '__main__':
    print(a(5, x(2), x(3), x(4), x(5), x(6)))