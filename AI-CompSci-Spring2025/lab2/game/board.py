class Board:
    def __init__(self, grid):
        self.grid = [row[:] for row in grid]
        self.rows = len(grid)
        self.cols = len(grid[0])
    def clone(self):
        return Board(self.grid)
    def get_moves(self, player):
        enemy = 'B' if player=='W' else 'W'
        moves = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j]==player:
                    for di,dj in [(1,0),(-1,0),(0,1),(0,-1)]:
                        ni,nj = i+di, j+dj
                        if 0<=ni<self.rows and 0<=nj<self.cols and self.grid[ni][nj]==enemy:
                            moves.append(((i,j),(ni,nj)))
        return moves
    def apply_move(self, move):
        (i,j),(ni,nj) = move
        p = self.grid[i][j]
        self.grid[i][j] = '_'
        self.grid[ni][nj] = p
    def is_terminal(self, player):
        return not self.get_moves(player)
    def winner(self, last_player):
        return last_player
    def __str__(self):
        return '\n'.join(' '.join(row) for row in self.grid)
