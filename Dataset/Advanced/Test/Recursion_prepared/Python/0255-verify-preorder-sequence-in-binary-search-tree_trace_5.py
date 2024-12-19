class Solution:
    def verifyPreorder(self, preorder: List[int]) -> bool:
        min_limit = -float("inf")
        stack = []
        
        for num in preorder:
            while stack and stack[-1] < num:
                min_limit = stack.pop()
                
            if num <= min_limit:
                return False
            
            stack.append(num)
        
        return True

if __name__ == "__main__":
    sol = Solution()
    print(sol.verifyPreorder([3, 2, 1, 5, 4, 6]))