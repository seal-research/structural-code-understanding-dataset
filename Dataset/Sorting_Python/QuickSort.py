def partition(array:List, left:int, right:int) -> int:
    # returns index of the pivot
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

    # when the loop breaks
    if pivot > array[high]:
        array[left], array[high] = array[high], array[left] # swap with the pivot
    # print(f"intermediate result\t{array}")
    return high


def quick_help(array:List, left:int, right:int) -> None:
    if left < right: # 정렬 범위가 2개 이상인 경우
        piv = partition(array, left, right)
        quick_help(array, left, piv-1)
        quick_help(array, piv+1, right)


def quick_sort(array:List) -> List:
    copied = array[:]
    quick_help(copied, 0, len(array)-1)
    return copied