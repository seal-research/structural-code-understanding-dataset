def shell_insert(array:list, last:int, gap:int) -> None:
    for i in range(last, 0, -gap):
        if array[i-gap] > array[i]:
            array[i-gap], array[i] = array[i], array[i-gap]


def shell_sort(array:list) -> list:
    copied = array[:]
    gap = len(copied) // 2
    i = 0
    while gap > 0:
        if i != 0 and gap % 2 == 0:
            gap += 1
        ## insertion sort ##
        for i in range(gap, len(copied)):
            shell_insert(copied, i, gap)
        gap = gap // 2
        i += 1
    return copied