def below_threshold(l: list, t: int):
    return all(i < t for i in l)