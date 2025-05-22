import sys,argparse
from game.board import Board
from game.agent import Agent

def parse_board(lines):
    return [line.split() for line in lines]

def create_default_board(rows=5, cols=6):
    board = []
    for i in range(rows):
        row = []
        for j in range(cols):
            # Black pieces on black fields (even sum of indices)
            # White pieces on white fields (odd sum of indices)
            piece = 'B' if (i+j) % 2 == 0 else 'W'
            row.append(piece)
        board.append(row)
    return board

def play(a1,a2,board,start,debug=False):
    player=start; last=None; nodes=0; dur=0; rounds=0
    
    # Store history of board states by creating a new Board with the same grid
    history = [(player, Board([row[:] for row in board.grid]))]
    
    if debug:
        print(f"Starting game with player {player}", file=sys.stderr)
        
    while True:
        moves=board.get_moves(player)
        if not moves: 
            if debug:
                print(f"Player {player} has no more moves. Game over.", file=sys.stderr)
            break
            
        agent=a1 if player=='B' else a2
        
        if debug:
            print(f"Round {rounds+1}: Player {player} thinking...", file=sys.stderr)
            print(f"Available moves: {moves}", file=sys.stderr)
            
        mv,n,n_dur=agent.move(board,player)
        
        if debug:
            print(f"Player {player} chose move: {mv}", file=sys.stderr)
            print(f"Nodes explored: {n}, Time taken: {n_dur:.4f}s", file=sys.stderr)
            
        board.apply_move(mv)
        
        # Store board state after move with a deep copy
        player = 'W' if player=='B' else 'B'  # Next player (for history record)
        history.append((player, Board([row[:] for row in board.grid])))
        
        if debug:
            print("Board after move:", file=sys.stderr)
            print(board, file=sys.stderr)
            print("-------------------", file=sys.stderr)
            
        nodes+=n; dur+=n_dur
        last=player
        rounds+=1
    
    return board,rounds,last,nodes,dur,history

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--mode',choices=['basic','ext'],default='basic')
    p.add_argument('--heur1',required=True)
    p.add_argument('--heur2',required=True)
    p.add_argument('--depth',type=int,required=True)
    p.add_argument('--method',choices=['minimax','alphabeta'],default='alphabeta')
    p.add_argument('--start',choices=['B','W'],default='B')
    p.add_argument('--debug',action='store_true',help='Enable debug output')
    p.add_argument('--history',action='store_true',help='Print board history to winning position')
    p.add_argument('--file',help='Input file with board configuration')
    args=p.parse_args()
    
    lines = []
    if args.file:
        with open(args.file, 'r') as f:
            lines = [l.strip() for l in f if l.strip()]
    else:
        # Try to read from stdin non-blocking
        import os
        if not os.isatty(sys.stdin.fileno()):
            import select
            if select.select([sys.stdin], [], [], 0.0)[0]:
                lines = [l.strip() for l in sys.stdin if l.strip()]
    
    if lines:
        grid=parse_board(lines)
    else:
        grid=create_default_board()
    
    board=Board(grid)
    
    if args.debug:
        print("=== INITIAL BOARD ===", file=sys.stderr)
        print(board, file=sys.stderr)
        print("====================", file=sys.stderr)
    
    a1=Agent('P1',args.method,args.heur1,args.depth)
    a2=Agent('P2',args.method,args.heur2,args.depth)
    
    b,rounds,last,nodes,dur,history=play(a1,a2,board,args.start,args.debug)
    print(b)
    print(f"{rounds} rounds, winner {last}")
    print(nodes,file=sys.stderr)
    print(f"{dur:.4f}",file=sys.stderr)
    
    # Print the history if requested
    if args.history:
        print("\n=== GAME HISTORY ===")
        for i, (next_player, board_state) in enumerate(history):
            if i == 0:
                print(f"Initial board (next player: {next_player}):")
            else:
                print(f"After move {i} (next player: {next_player}):")
            print(board_state)
            print("-------------------")

if __name__=='__main__':
    main()
