def bubble(array:List, idx:int) -> None:
    last = len(array) - idx
    for i in range(last-1):
        if array[i] > array[i+1]:
            array[i], array[i+1] = array[i+1], array[i]


def bubble_sort(array:List) -> List:
    copied = array[:]
    for i in range(len(copied)):
        bubble(copied, i)
    return copied