def anti_shuffle(s):
    return''.join(''.join(sorted(word, key=lambda x: (not x.isalpha(), x.lower()))) for word in s.split(' '))