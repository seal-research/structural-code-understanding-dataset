def is_nested(string):
    stack = []
    for char in string:
        if char == '[':
            stack.append(char)
        elif char == ']':
            if len(stack) > 1:
                return True
            if not stack:
                return False
            stack.pop()
    return False