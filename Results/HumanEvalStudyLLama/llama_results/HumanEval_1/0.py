from typing import List

def separate_paren_groups(paren_string: str) -> List[str]:
    paren_string = paren_string.replace(' ', '')
    result = []
    temp = ''
    count = 0
    for char in paren_string:
        temp += char
        if char == '(':
            count += 1
        else:
            count -= 1
        if count == 0:
            result.append(temp)
            temp = ''
    return result