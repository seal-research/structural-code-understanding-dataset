# since heap can be implemented as an array, let's define a function that modifies an array to a heap
def min_heapify(array:List, root:int, last:int) -> None:
    smallest = root
    left_child = (2 * root) + 1
    right_child = (2 * root) + 2

    # check if there is any child whose value is smaller than the parent
    if left_child < last and array[left_child] < array[smallest]:
        smallest = left_child
    if right_child < last and array[right_child] < array[smallest]:
        smallest = right_child
    
    # if larger child exists, change
    if smallest != root:
        array[root], array[smallest] = array[smallest], array[root]
        # recursively modify the affected subtree
        min_heapify(array, smallest, last)


def min_heap_sort(array:List) -> List:
    copied = array[:]
    size = len(copied)
    
    # build heap
    for i in range(len(copied)//2-1, -1, -1):
        min_heapify(copied, i, len(copied))

    # pop
    for i in range(len(copied)-1, 0, -1):
        copied[0], copied[i] = copied[i], copied[0]
        size -= 1
        min_heapify(copied, 0, size)
    return copied