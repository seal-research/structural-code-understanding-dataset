def how_many_times(string: str, substring: str) -> int:
    count = 0
    start = 0
    while start < len(string):
        pos = string.find(substring, start)
        if pos!= -1:
            count += 1
            start = pos + 1
        else:
            break
    return count