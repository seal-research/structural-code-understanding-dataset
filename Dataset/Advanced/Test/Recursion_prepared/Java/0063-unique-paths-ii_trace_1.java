class Solution {
    public int uniquePathsWithObstacles(int[][] grid) {
        return dfs(
            grid,
            0,
            0,
            grid.length,
            grid[0].length,
            new int[grid.length][grid[0].length]
        );
    }

    public int dfs(int[][] grid, int i, int j, int m, int n, int[][] dp) {
        if (i < 0 || j < 0 || i >= m || j >= n || grid[i][j] == 1) {
            return 0;
        }
        if (i == m - 1 && j == n - 1) {
            dp[i][j] = 1;
            return dp[i][j];
        }
        if (dp[i][j] != 0) return dp[i][j];
        int right = dfs(grid, i, j + 1, m, n, dp);
        int left = dfs(grid, i + 1, j, m, n, dp);
        dp[i][j] = right + left;
        return dp[i][j];
    }

    public static void main(String[] args) {
        Solution sol = new Solution();
        int[][] grid = {{0, 0, 0}, {0, 1, 0}, {0, 0, 0}};
        System.out.println(sol.uniquePathsWithObstacles(grid)); // Output: 2
    }
}