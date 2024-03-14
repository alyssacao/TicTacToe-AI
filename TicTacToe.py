import sys

# Parse command line arguments
if len(sys.argv) != 4:
    print("Not enough/ too many/ illegal input arguments")
    sys.exit(1)
    
# Get information from command line
# Algorithm: 1. Minimax vs. 2.Minimax with Alpha - Beta
# First: Which player move first: X or O
# Mode: Human vs. Computer or Computer vs. Computer
algo = sys.argv[1]
first = sys.argv[2]
mode = sys.argv[3]

# Display information before the game
print(f"Algorithm: {'MiniMax Search' if algo == '1' else 'MiniMax with alpha-beta pruning'}")
print(f"First: {first}")
print(f"Mode: {'human (X)' if mode == '1' else 'computer (X)'} versus  computer (O)")

# Initialize the game board
board = [' '] * 9
# Set current player equal to first
current_player = first

# Display TicTacToe board
def display_board(board):
    for i in range(0,9,3):
        print(f"{board[i]}  | {board [i+1]} | {board[i+2]}")
        if i<6:
            print("---+---+---")
            
# Decide and return whose move
def game_to_move(state, first):
    # Count the number of 'X' and 'O in the game state
    count_x = state.count('X')
    count_o = state.count('O')
    if count_x == count_o:
        # If 'X' and "O" cunts are equal, return the first player
        if first == 'X':
            return 'X'
        else: 
            return 'O'
    if count_x > count_o:
        # If 'X' count is greater than 'O', it's O's turn
        return 'O'
    if count_x < count_o:
        # If 'O' count is greater than 'X', it's X's turn
        return 'X'

# Check if the game is over   
def is_terminal(state, player):
    # Possible winning combinations in the game
    win_combos = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
    if player == 'X':
        opponent = 'O'
    if player == 'O':
        opponent = 'X'
    for a, b, c in win_combos:
        # Check if the current player has won the game and return win
        if state[a] == state[b] == state[c] and state[a] == player:
            return (True, 'win', state[a])
        # Check if the opponent has won the game and return loss
        if state[a] == state[b] == state[c] and state[a] == opponent:
            return (True, 'loss', state[a]) 
    # If no one has won and all cells are filled, return tie
    if all(state[cell] != ' ' for cell in range(1,9)):
        return (True, 'tie', None) 
    # The game is not over yet
    return (False, 'neither', None) 

# Represent game outcome by checking if the game is over
def is_terminal2(state, player):
    win_combos = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
    if player == 'X':
        opponent = 'O'
    if player == 'O':
        opponent = 'X'
    for a, b, c in win_combos:
        # Return 1 if current player has won
        if state[a] == state[b] == state[c] and state[a] == player:
            return (True, 1)
        # Return -1 if the opponent has won
        if state[a] == state[b] == state[c] and state[a] == opponent:
            return (True, -1) 
    # Return 0 if the game is tie
    if all(state[cell] != ' ' for cell in range(1,9)):
        return (True, 0) 
    # Return None otherwise
    return (False, None) 

# Utility for each player
def utility(state, player):
    result, game_result, winning_player = is_terminal(state, player)
    if result:
        # Return 1 if the game state is win
        if game_result == 'win':
            return 1  
        # Return -1 if the game state is loss
        if game_result == 'loss':
            return -1  
        # Return 0 if teh game state is tie
        if game_result == 'tie':
            return 0
    else:
        return None
      
# Possible moves 
def actions(state):
    # Create a list of valid actions on the game board
    valid_actions = [action + 1 for action in range(9) if state[action] == ' ']
    return sorted(valid_actions)

# Update the state of the board
def result(state, action, first):
    # Copying the original state
    new_state = state.copy()
    # Create new game state by updating with current player's move
    new_state[action - 1] = game_to_move(state, first)
    return new_state

# Minimax Search
def minimax_search(state, first):
    # Determine the current player
    player = game_to_move(state, first)
    # Initialize the counter for the number of nodes explored
    nodes = 0
    # Perform a max value search to find the best move
    value, move, nodes = max_value(state, player, nodes, first) 
    return move, nodes
        
        
def max_value(state, player, nodes, first):
    # Increment the node count for the current level of the tree
    nodes += 1
    # Check if the current state is terminal
    (is_terminal, utility) = is_terminal2(state, player)
    if is_terminal:
        return (utility, None, nodes)
    # Initialize v to negative infinity (worst value for max player)
    v = float('-inf')
    for a in actions(state):
        v2, a2, nodes = min_value(result(state, a, first), player, nodes, first)
        if v2 > v:
            v = v2 # Update c with the max value found so far
            move = a # Update the move corresponding to the max value
    return v, move, nodes


def min_value(state, player, nodes, first):
    # Increment the node count for the current level of the tree
    nodes += 1
    # Check if the current state is terminal
    (is_terminal, utility) = is_terminal2(state, player)
    if is_terminal:
        return (utility, None, nodes)
    # Initialize v to positive infinity (best value of min player)
    v = float('inf')
    for a in actions(state):
        
        v2, a2 , nodes = max_value(result(state, a, first), player, nodes, first)
        if v2 < v:
            v = v2  # Update v with the min value so far
            move = a # Update the move corresponding to the min value
    return v, move, nodes

# Minimax Search with alpha-beta pruning
def alpha_beta(state, first):
    # Determine the current player
    player = game_to_move(state, first)
    # Initialize the counter for the number of nodes explored
    nodes = 0
    # Perform a max value with alpha beta search to find the best move
    value, move, nodes = max_value_ab(state, player, float('-inf'), float('inf'), nodes, first)
    return move, nodes

def max_value_ab(state, player, alpha, beta, nodes, first):
    # Increment the node count for the current level of the tree
    nodes += 1
    (is_terminal, utility) = is_terminal2(state,player)
    if is_terminal:
        return (utility, None, nodes)
    # Initialize v to negative infinity (worst value for max player)
    v = float('-inf')
    for a in actions(state):
        v2, a2 , nodes = min_value_ab(result(state, a, first), player, alpha, beta, nodes, first)
        if v2 > v:
            v, move = v2, a
            alpha = max(alpha, v)
        if v >= beta:
            return v, move, nodes
    return v, move, nodes
        
def min_value_ab(state, player, alpha, beta, nodes, first):
    # Increment the node count for the current level of the tree
    nodes += 1
    (is_terminal, utility) = is_terminal2(state, player)
    if is_terminal:
        return (utility, None, nodes)
    # Initialize v to positive infinity (best value of min player)
    v = float('inf')
    for a in actions(state):
        v2, a2, nodes = max_value_ab(result(state, a, first), player, alpha, beta, nodes, first)
        if v2 < v :
            v, move = v2, a
            beta = min(beta, v)
        if v <= alpha:
            return v, move, nodes
    return v, move, nodes

# Start the game
while True:
    # Display the current state of the game board
    display_board(board)
    if current_player == 'X' and mode == '1': # If it is human's  turn
        # Get a list of available moves for teh current board
        available_moves = actions(board)
        while True:
            move = int(input(f"{current_player}'s move. What is your move (possible moves at the moment are: {', '.join(map(str, available_moves))} | enter 0 to exit the game)? "))                   
            if move in available_moves:
                board = result(board, move, first)  # Update the board after a valid move
                break
            elif move == 0:
                sys.exit(0) # Exit the game if user enters 0
            else:
                print("Invalid move. Please enter a valid move.")
    else:
        print("algo" + str(algo))
        # If computer using minimax search
        if algo == '1': 
            print(actions(board))
            # Find the best move using minimax
            (cmove, nodes) = minimax_search(board, first)
            print(f"Computer's move of minimax: {cmove}")
            # Update the board after current move
            print(game_to_move(board, print))
            print(utility(board, current_player))
            board = result(board, cmove, first)                   
            print(f"{current_player}'s minimax selected move: {cmove }. Number of search tree nodes generated: ", nodes)
        #Computer's turn using alpha-beta
        else:  
            print(actions(board))
            # Find teh best move using alpha-beta search
            (cmove, nodes) = alpha_beta(board, first)
            print("alpha beta")
            print(f"Computer's move of alha-beta: {cmove}")
            # Update the board adter current mvoe
            print(game_to_move(board, print))
            print(utility(board, current_player))
            board = result(board, cmove, first)               
            print(f"{current_player}'s selected move: {cmove }. Number of search tree nodes generated: ", nodes) 

    # Check if the game is in terminal state   
    final = is_terminal(board, current_player)
    if final[0]:
        # Display the final state of the game board
        display_board(board) 
        if final[1] == 'win':
            if final[2] == current_player:
                print(f"{current_player} won!")
                if current_player == 'X':
                    print("O lost!")
                else:
                    print("X lost!")
        elif final[1] == 'tie':
                print("It's a tie!")    
        # Exit the loop if the game is over
        break
    # Alternate players
    current_player = game_to_move(board, first)
    
        