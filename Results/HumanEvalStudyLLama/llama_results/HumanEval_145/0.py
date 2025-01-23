def order_by_points(nums):
    def sum_of_digits(num):
        return sum(int(digit) for digit in str(abs(num)))

    return sorted(enumerate(nums), key=lambda x: (sum_of_digits(x[1]), x[0]))