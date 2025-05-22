from utils import Timer
from .board import Board
def alphabeta(board:Board, player, depth, heur):
    nodes=0
    
    # Define the alpha-beta function without the Timer decorator
    def _ab_core(node, pl, d, a, b):
        nonlocal nodes
        nodes+=1
        if d==0 or node.is_terminal(pl):
            return heur(node,pl),None
        best_mv=None
        if pl==player:
            val=float('-inf')
            for mv in node.get_moves(pl):
                nb=node.clone(); nb.apply_move(mv)
                v,_=_ab_core(nb,'B' if pl=='W' else 'W',d-1,a,b)
                if v>val: val,best_mv=v,mv
                a=max(a,val)
                if a>=b: break
            return val,best_mv
        else:
            val=float('inf')
            for mv in node.get_moves(pl):
                nb=node.clone(); nb.apply_move(mv)
                v,_=_ab_core(nb,'B' if pl=='W' else 'W',d-1,a,b)
                if v<val: val,best_mv=v,mv
                b=min(b,val)
                if b<=a: break
            return val,best_mv
    
    # Use Timer only on the initial call, not on recursive calls
    @Timer
    def _ab_timed():
        return _ab_core(board,player,depth,float('-inf'),float('inf'))
        
    (val,mv),dur=_ab_timed()
    return mv,nodes,dur
