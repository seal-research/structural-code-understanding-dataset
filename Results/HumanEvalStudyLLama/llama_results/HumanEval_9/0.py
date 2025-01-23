from typing import List

def rolling_max(numbers: List[int]) -> List[int]:
    if not numbers:
        return []
    
    max_so_far = numbers[0]
    result = [max_so_far]
    
    for num in numbers[1:]:
        max_so_far = max(max_so_far, num)
        result.append(max_so_far)
    
    return result