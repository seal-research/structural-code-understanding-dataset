def merge(array:list, start:int, mid:int, last:int) -> None:
    k = start

    sub1, sub2 = array[start:mid+1], array[mid+1:last+1]
    
    i = j = 0
    while i < len(sub1) and j < len(sub2):
        if sub1[i] > sub2[j]:
            array[k] = sub2[j] 
            j += 1
        else:
            array[k] = sub1[i]
            i += 1
        k += 1
    
    if i == len(sub1):
        array[k:last+1] = sub2[j:]
    else:
        array[k:last+1] = sub1[i:]


def merge_help(array:list, start:int, last:int) -> None:
    if start == last:
        return
    else:
        mid = (start + last) // 2
        merge_help(array, start, mid)
        merge_help(array, mid+1, last)
        merge(array, start, mid, last)


def merge_sort(array:list) -> list:
    copied = array[:]
    merge_help(copied, 0, len(array)-1)
    return copied