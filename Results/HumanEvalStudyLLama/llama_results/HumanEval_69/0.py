from collections import Counter

def search(lst):
    count = Counter(lst)
    for i in sorted(count, reverse=True):
        if count[i] >= i:
            return i
    return -1