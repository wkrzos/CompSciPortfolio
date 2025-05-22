from .board import Board
def h_count(board:Board, player):
    enemy = 'B' if player=='W' else 'W'
    pc = sum(row.count(player) for row in board.grid)
    ec = sum(row.count(enemy) for row in board.grid)
    return pc-ec
def h_mobility(board:Board, player):
    enemy = 'B' if player=='W' else 'W'
    return len(board.get_moves(player))-len(board.get_moves(enemy))
def h_combo(board:Board, player):
    return h_count(board,player)*2 + h_mobility(board,player)
HEURISTICS = {'count':h_count,'mobility':h_mobility,'combo':h_combo}
