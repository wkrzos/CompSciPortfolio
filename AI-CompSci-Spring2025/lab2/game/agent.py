from .heuristics import HEURISTICS
from .minimax import minimax
from .alphabeta import alphabeta
class Agent:
    def __init__(self, name, method, heur_name, depth):
        self.name=name
        self.method=method
        self.heur=HEURISTICS[heur_name]
        self.depth=depth
    def move(self, board, player):
        if self.method=='minimax':
            return minimax(board,player,self.depth,self.heur)
        return alphabeta(board,player,self.depth,self.heur)
