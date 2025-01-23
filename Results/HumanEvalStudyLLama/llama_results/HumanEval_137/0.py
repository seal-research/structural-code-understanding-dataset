def compare_one(a, b):
    def convert_to_float(x):
        if isinstance(x, str):
            return float(x.replace(',', '.'))
        else:
            return float(x)

    a_float = convert_to_float(a)
    b_float = convert_to_float(b)

    if a_float > b_float:
        if isinstance(a, str):
            return a.replace('.', ',')
        else:
            return a
    elif a_float < b_float:
        if isinstance(b, str):
            return b.replace('.', ',')
        else:
            return b
    else:
        return None