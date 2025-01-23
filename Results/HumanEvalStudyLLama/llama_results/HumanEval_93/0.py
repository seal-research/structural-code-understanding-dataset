def encode(message):
    vowels = 'aeiouAEIOU'
    shifted_vowels = 'cdeoCDEO'
    encoded_message = ''
    for char in message:
        if char in vowels:
            encoded_message += shifted_vowels[vowels.index(char)]
        else:
            encoded_message += char.swapcase()
    return encoded_message