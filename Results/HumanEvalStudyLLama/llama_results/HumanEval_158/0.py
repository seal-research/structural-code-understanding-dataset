def find_max(words):
    def unique_chars(word):
        return len(set(word))

    max_unique = max(unique_chars(word) for word in words)
    max_words = [word for word in words if unique_chars(word) == max_unique]
    return min(max_words)