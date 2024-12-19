class Solution {
    public int count(int [][]board){
        int c = 0;
        for(int i=0; i<board.length; i++){
            for(int j=0; j<board[0].length; j++){
                if(board[i][j] == 1){
                    c++;
                }
            }
        }
        return c;
    }
    public void dfs(int r, int c, int[][] board){
        if(r<0 || c<0 || r>board.length-1 || c>board[0].length-1 || board[r][c] != 1) return;

        board[r][c] = 2;

        dfs(r+1, c, board);
        dfs(r-1, c, board);
        dfs(r, c+1, board);
        dfs(r, c-1, board);
    }
    public int numEnclaves(int[][] board) {
        int n=board.length, m=board[0].length;

        for(int i=0; i<n; i++){
            if(board[i][0] == 1) dfs(i, 0, board);
            if(board[i][m-1] == 1) dfs(i, m-1, board);
        }

        for(int i=1; i<m-1; i++){
            if(board[0][i] == 1) dfs(0, i, board);
            if(board[n-1][i] == 1) dfs(n-1, i, board);
        }
        return count(board);
    }

    public static void main(String[] args) {
        Solution sol = new Solution();
        int[][] board = {
            {0, 0, 0, 0},
            {0, 0, 0, 0},
            {0, 0, 0, 0},
            {0, 0, 0, 0}
        };
        System.out.println(sol.numEnclaves(board));
    }
}