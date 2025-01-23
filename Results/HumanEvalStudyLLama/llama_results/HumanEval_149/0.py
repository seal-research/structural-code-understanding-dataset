def sorted_list_sum(lst):
    return sorted([s for s in lst if len(s) % 2 == 0], key=lambda x: (len(x), x))