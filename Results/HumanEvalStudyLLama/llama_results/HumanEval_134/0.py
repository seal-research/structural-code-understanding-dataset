def check_if_last_char_is_a_letter(txt):
    if not txt:
        return False
    if txt[-1] =='':
        return False
    words = txt.split()
    last_word = words[-1]
    return len(last_word) == 1 and last_word.isalpha()