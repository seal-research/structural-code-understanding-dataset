def lcm(a, b, multiple=None):
    # Initialize the multiple on the first call as the larger of a or b
    if multiple is None:
        multiple = max(a, b)
    
    # Base case: if the multiple is divisible by both a and b, return it as the LCM
    if multiple % a == 0 and multiple % b == 0:
        return multiple
    
    # Recursive case: increment the multiple by max(a, b) and call lcm again
    return lcm(a, b, multiple + max(a, b))

if __name__ == "__main__":
    print(lcm(21, 6))