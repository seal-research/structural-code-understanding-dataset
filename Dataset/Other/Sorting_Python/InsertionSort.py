def insert(array:list, last:int) -> None:
    for i in range(last, 0, -1):
        if array[i-1] > array[i]:
            array[i-1], array[i] = array[i], array[i-1]


def insertion_sort(array:list) -> list:
    copied = array[:]
    for i in range(1, len(copied)):
        insert(copied, i)
    return copied