from game import *
import random
import numpy as np

# Define the possible moves
move_options = [0, 1, 2, 3]

# Function to randomly select a move
def choose_random_move():
    return random.choice(move_options)

# Function to calculate the highest tile on the board
def find_max_tile(board):
    return max(max(row) for row in board)

# Main game loop
def run_simulation():
    game_count = 10000
    game_scores = np.zeros(game_count)
    highest_tiles = np.zeros(game_count)
    
    for idx in range(game_count):
        board = new_game(4)  # Start a new game with a 4x4 board
        board = add_two(board)  # Add the first tile
        board = add_two(board)  # Add the second tile
        game_over = False
        
        while not game_over:
            move = choose_random_move()  # Select a random move
            board, score = perform_move(board, move)  # Apply the move
            game_scores[idx] += score
            board = add_two(board)  # Add a new tile after the move
            
            if game_state(board) == 'lose':
                highest_tiles[idx] = find_max_tile(board)  # Record the highest tile reached
                game_over = True
        
    # Output results
    print(f"Average score: {game_scores.mean()}")
    print(f"Standard deviation of scores: {game_scores.std()}")
    
    # Calculate and print the frequency of reaching each tile
    print("Frequency of reaching tiles:")
    highest_tile_value = int(highest_tiles.max())
    while highest_tile_value >= 2:
        frequency = np.sum(highest_tiles >= highest_tile_value) / game_count
        print(f"{highest_tile_value}: {frequency:.4f}")
        highest_tile_value //= 2

if __name__ == "__main__":
    run_simulation()
