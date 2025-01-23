from typing import List

def remove_duplicates(numbers: List[int]) -> List[int]:
    seen = set()
    seen_twice = set()
    result = []
    for num in numbers:
        if num in seen_twice:
            continue
        elif num in seen:
            seen_twice.add(num)
        else:
            seen.add(num)
            result.append(num)
    return result