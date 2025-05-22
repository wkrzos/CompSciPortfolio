import time
from utils import Timer
from .board import Board
def minimax(board:Board, player, depth, heur):
    nodes=0
    
    # Define a recursive minimax function without the Timer decorator
    def _minimax_core(node, pl, d):
        nonlocal nodes
        nodes+=1
        if d==0 or node.is_terminal(pl):
            return heur(node,pl),None
        best_val, best_mv = (float('-inf'),None) if pl==player else (float('inf'),None)
        for mv in node.get_moves(pl):
            nb = node.clone(); nb.apply_move(mv)
            val, _ = _minimax_core(nb, 'B' if pl=='W' else 'W', d-1)
            if pl==player and val>best_val or pl!=player and val<best_val:
                best_val,best_mv = val,mv
        return best_val,best_mv
    
    # Use Timer only on the initial call, not on recursive calls
    @Timer
    def _minimax_timed():
        return _minimax_core(board, player, depth)
    (best_val, best_mv), dur = _minimax_timed()
    return best_mv, nodes, dur
