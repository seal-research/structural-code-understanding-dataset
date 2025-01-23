def largest_smallest_integers(lst):
    negatives = [i for i in lst if i < 0]
    positives = [i for i in lst if i > 0]
    if negatives:
        a = max(negatives)
    else:
        a = None
    if positives:
        b = min(positives)
    else:
        b = None
    return (a, b)