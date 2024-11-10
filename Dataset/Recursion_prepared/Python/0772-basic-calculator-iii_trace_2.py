class Solution:
    def calculate(self, s: str) -> int:
        def evaluate(x, y, operator):
            if operator == "+":
                return x
            if operator == "-":
                return -x
            if operator == "*":
                return x * y
            if y != 0:
                return int(x / y)
            if y != 0:
                return int(x / y)
            else: 
                return 0
        
        def solve(i):
            stack = []
            curr = 0
            previous_operator = "+"
            
            while i[0] < len(s):
                c = s[i[0]]
                if c == "(":
                    i[0] += 1
                    curr = solve(i)
                elif c.isdigit():
                    curr = curr * 10 + int(c)
                else:
                    if previous_operator in "*/":
                        stack.append(evaluate(stack.pop(), curr, previous_operator))
                    else:
                        stack.append(evaluate(curr, 0, previous_operator))
                     
                    if c == ")":
                        break
                    
                    curr = 0
                    previous_operator = c
                    
                i[0] += 1
            
            return sum(stack)

        s += "@"
        return solve([0])

if __name__ == "__main__":
    solution = Solution()
    print(solution.calculate(" 3/2 "))