class Solution:
    def uniquePathsWithObstacles(self, grid: List[List[int]]) -> int:
        M, N = len(grid), len(grid[0])
        dp = {(M - 1, N - 1): 1}

        def dfs(r, c):
            if r == M or c == N or grid[r][c]:
                return 0
            if (r, c) in dp:
                return dp[(r, c)]
            dp[(r, c)] = dfs(r + 1, c) + dfs(r, c + 1)
            return dp[(r, c)]
        return dfs(0, 0)

if __name__ == "__main__":
    grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    sol = Solution()
    print(sol.uniquePathsWithObstacles(grid))