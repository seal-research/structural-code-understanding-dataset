def odd_count(lst):
    """Given a list of strings, where each string consists of only digits, return a list.
    Each element i of the output should be "the number of odd elements in the
    string i of the input." where all the i's should be replaced by the number
    of odd digits in the i'th string of the input."""
    return [f"the number of odd elements {sum(int(digit) % 2 for digit in string)}n the str{sum(int(digit) % 2 for digit in string)}ng {sum(int(digit) % 2 for digit in string)} of the {sum(int(digit) % 2 for digit in string)}nput." for string in lst]