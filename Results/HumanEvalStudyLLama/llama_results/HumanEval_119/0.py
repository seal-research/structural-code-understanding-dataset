def match_parens(lst):
    def is_balanced(s):
        stack = []
        for char in s:
            if char == '(':
                stack.append(char)
            elif char == ')':
                if not stack:
                    return False
                stack.pop()
        return not stack

    return 'Yes' if is_balanced(lst[0] + lst[1]) or is_balanced(lst[1] + lst[0]) else 'No'