def partition(array:list, left:int, right:int) -> int:
    pivot = array[left]
    low = left + 1
    high = right
    while low < high:
        while array[low] < pivot and low < right:
            low += 1
        while array[high] > pivot and high > left:
            high -= 1
        if low < high:
            array[low], array[high] = array[high], array[low]

    if pivot > array[high]:
        array[left], array[high] = array[high], array[left]
    return high


def quick_help(array:list, left:int, right:int) -> None:
    if left < right:
        piv = partition(array, left, right)
        quick_help(array, left, piv-1)
        quick_help(array, piv+1, right)


def quick_sort(array:list) -> list:
    copied = array[:]
    quick_help(copied, 0, len(array)-1)
    return copied