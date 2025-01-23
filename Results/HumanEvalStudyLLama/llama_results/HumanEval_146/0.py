def specialFilter(nums):
    def is_odd_digit(n):
        return str(abs(n))[0] in '13579' and str(abs(n))[-1] in '13579'

    return sum(1 for num in nums if num > 10 and is_odd_digit(num))