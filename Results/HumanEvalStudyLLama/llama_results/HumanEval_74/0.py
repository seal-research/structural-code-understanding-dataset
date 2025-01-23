def total_match(lst1, lst2):
    def total_chars(lst):
        return sum(len(s) for s in lst)

    if total_chars(lst1) <= total_chars(lst2):
        return lst1
    else:
        return lst2