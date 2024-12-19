def is_palindrome(s):
    # Base case: if the string is empty or has one character, it's a palindrome
    if len(s) <= 1:
        return True
    # Check if the first and last characters are the same
    if s[0] != s[-1]:
        return False
    # Recursive case: check the substring without the first and last characters
    return is_palindrome(s[1:-1])

if __name__ == "__main__":
  print(is_palindrome("hello"))