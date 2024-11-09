class Solution:
    def solve(self, board: List[List[str]]) -> None:
        rows, cols = len(board), len(board[0])
        flag = set()

        def dfs(r, c):
            if not(r in range(rows) and c in range(cols)) or board[r][c] != 'O' or (r, c) in flag:
                return
            flag.add((r, c))
            return (dfs(r + 1, c), dfs(r - 1, c), dfs(r, c + 1), dfs(r, c - 1))

        # traverse through the board
        for r in range(rows):
            for c in range(cols):
                if( (r == 0 or c == 0 or r == rows - 1 or c == cols - 1) and board[r][c] == 'O'):
                    dfs(r, c)

        # set all of the 'X's to 'O's
        for r in range(rows):
            for c in range(cols):
                if board[r][c] == 'O' and (r, c) not in flag:
                    board[r][c] = 'X'

if __name__ == "__main__":
    board = [
        ["O", "O", "O", "O"],
        ["O", "X", "X", "O"],
        ["O", "X", "X", "O"],
        ["O", "O", "O", "O"]
    ]
    Solution().solve(board)
    print(board)