def sort_array(arr):
    return sorted(arr, key=lambda x: (bin(abs(x)).count('1'), abs(x)))