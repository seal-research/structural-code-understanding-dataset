class MyPolynomial:
    def __init__(self, *coeffs):
        self.coeffs = coeffs

    def get_coeffs(self):
        return self.coeffs

    def set_coeffs(self, coeffs):
        self.coeffs = coeffs

    def get_degree(self):
        return len(self.coeffs) - 1

    def __str__(self):
        coeffs_string = ""
        for degree in range(len(self.coeffs) - 1, -1, -1):
            if self.coeffs[degree] == 0:
                continue
            if degree == len(self.coeffs) - 1:
                coeffs_string += str(round(self.coeffs[degree], 2))
            else:
                coeffs_string += " + " if self.coeffs[degree] > 0 else " - "
                coeffs_string += str(abs(round(self.coeffs[degree], 2)))

            if degree >= 2:
                coeffs_string += f"x^{degree}"
            elif degree == 1:
                coeffs_string += "x"
        return coeffs_string

    def evaluate(self, x):
        ans = 0
        for degree in range(len(self.coeffs)):
            ans += (self.coeffs[degree] * (x ** degree))
        return ans

    def add(self, another):
        size = max(len(self.coeffs), another.get_degree() + 1)
        ans = [0] * size

        for degree in range(size):
            add = 0
            if degree <= self.get_degree():
                add += self.coeffs[degree]
            if degree <= another.get_degree():
                add += another.coeffs[degree]
            ans[degree] = add

        return MyPolynomial(*ans)

    def multiply(self, another):
        size = self.get_degree() + another.get_degree() + 1
        ans = [0] * size

        for deg1 in range(len(self.coeffs)):
            for deg2 in range(len(another.coeffs)):
                num = self.coeffs[deg1] * another.coeffs[deg2]
                ans[deg1 + deg2] += num

        return MyPolynomial(*ans)

if __name__ == "__main__":
    p2 = MyPolynomial(1.0, 0.0, 5.0, 0.0)
    p2.set_coeffs([0.0, 3.0, 0.0, 2.0])
    print(p2.get_coeffs())
    print(p2)