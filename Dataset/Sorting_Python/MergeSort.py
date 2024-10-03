def merge(array:List, start:int, mid:int, last:int) -> None:
    # declare an integer to indicate the index of the original array
    # this is kind of a detour of declaring a new array
    k = start

    # divide the array
    sub1, sub2 = array[start:mid+1], array[mid+1:last+1]
    
    # iterate the loop until either one becomes empty
    i = j = 0
    while i < len(sub1) and j < len(sub2):
        if sub1[i] > sub2[j]:
            array[k] = sub2[j] # this substitution is equivalent to appending the value to the new array
            j += 1
        else:
            array[k] = sub1[i]
            i += 1
        k += 1 # for any case, k should increase
    
    # if the loop is over, either i == len(sub1) or j == len(sub2)
    if i == len(sub1): # sub1 is empty
        array[k:last+1] = sub2[j:]
    else:
        array[k:last+1] = sub1[i:]


def merge_help(array:List, start:int, last:int) -> None:
    # verifying if the len(array) is 1
    if start == last:
        return # do nothing
    else:
        mid = (start + last) // 2
        merge_help(array, start, mid)
        merge_help(array, mid+1, last)
        merge(array, start, mid, last)


def merge_sort(array:List) -> List:
    copied = array[:]
    merge_help(copied, 0, len(array)-1)
    return copied