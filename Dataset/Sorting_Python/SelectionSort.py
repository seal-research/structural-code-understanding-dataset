def smallest(array:List, start:int) -> int:
    smallest = start
    for i in range(start, len(array)):
        if array[smallest] > array[i]:
            smallest = i
    return smallest


def selection_sort(array:List) -> List:
    copied = array[:]
    for i in range(len(copied)):
        small_idx = smallest(copied, i)
        if copied[small_idx] < copied[i]:
            copied[small_idx], copied[i] = copied[i], copied[small_idx]
    return copied