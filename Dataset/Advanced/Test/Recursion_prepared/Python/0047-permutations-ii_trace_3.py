import collections
from typing import List

class Solution:

    def permuteUnique(self, nums: List[int]) -> List[List[int]]:
        result = []
        counter = collections.Counter(nums)

        def backtrack(perm, counter):
            if len(perm) == len(nums):
                result.append(perm.copy())

            for n in counter:
                if counter[n] == 0:
                    continue
                perm.append(n)
                counter[n] -= 1
                backtrack(perm, counter)
                perm.pop()
                counter[n] += 1

        backtrack([], counter)

        return result

if __name__ == "__main__":
    sol = Solution()
    print(sol.permuteUnique([2, 2, 1, 1]))