def split_words(txt):
    if'' in txt:
        return txt.split()
    elif ',' in txt:
        return txt.split(',')
    else:
        return sum(1 for i, c in enumerate(txt.lower()) if c.isalpha() and ord(c) % 2!= 0)