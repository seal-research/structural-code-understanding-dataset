def bubble(array:list, idx:int) -> None:
    last = len(array) - idx
    for i in range(last-1):
        if array[i] > array[i+1]:
            array[i], array[i+1] = array[i+1], array[i]


def bubble_sort(array:list) -> list:
    copied = array[:]
    for i in range(len(copied)):
        bubble(copied, i)
    return copied

if __name__ == '__main__':
    bubble_sort([5,4,6,6,4,2,4,5,3,2,3,4,3,2,1,6])
