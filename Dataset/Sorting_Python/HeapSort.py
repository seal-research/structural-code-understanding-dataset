def min_heapify(array:List, root:int, last:int) -> None:
    smallest = root
    left_child = (2 * root) + 1
    right_child = (2 * root) + 2

    if left_child < last and array[left_child] < array[smallest]:
        smallest = left_child
    if right_child < last and array[right_child] < array[smallest]:
        smallest = right_child
    
    if smallest != root:
        array[root], array[smallest] = array[smallest], array[root]
        min_heapify(array, smallest, last)


def min_heap_sort(array:List) -> List:
    copied = array[:]
    size = len(copied)
    
    for i in range(len(copied)//2-1, -1, -1):
        min_heapify(copied, i, len(copied))

    for i in range(len(copied)-1, 0, -1):
        copied[0], copied[i] = copied[i], copied[0]
        size -= 1
        min_heapify(copied, 0, size)
    return copied