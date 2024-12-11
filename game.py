#Game.py
import numpy as np
import random

# Initialize a new game board
def new_game(size):
    return np.zeros((size, size), dtype=int)

# Retrieve empty cells from the board
def get_empty_cells(board):
    return [(i, j) for i in range(len(board)) for j in range(len(board[0])) if board[i][j] == 0]

# Add a new tile (2 or 4) to a random empty cell
def add_two(board):
    empty_cells = get_empty_cells(board)
    if not empty_cells:
        return board

    row, col = random.choice(empty_cells)
    board[row][col] = 4 if random.random() >= 0.9 else 2
    return board

# Check the game state (win, lose, or ongoing)
def game_state(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return 'not over'

            if i < len(board) - 1 and board[i][j] == board[i + 1][j]:
                return 'not over'

            if j < len(board[0]) - 1 and board[i][j] == board[i][j + 1]:
                return 'not over'

    return 'lose'

# Reverse the rows of the board
def reverse(board):
    return np.flip(board, axis=1)

# Transpose the board
def transpose(board):
    return board.T

# Cover up zeros to the left
def cover_up(board):
    new_board = np.zeros_like(board)
    done = False

    for i in range(len(board)):
        position = 0
        for j in range(len(board[0])):
            if board[i][j] != 0:
                new_board[i][position] = board[i][j]
                if j != position:
                    done = True
                position += 1

    return new_board, done

# Merge tiles
def merge(board):
    done = False
    score = 0

    for i in range(len(board)):
        for j in range(len(board[0]) - 1):
            if board[i][j] == board[i][j + 1] and board[i][j] != 0:
                board[i][j] *= 2
                score += board[i][j]
                board[i][j + 1] = 0
                done = True

    return board, done, score

# Perform a move in a specific direction
def perform_move(board, move):
    if move == 0:  # Up
        board = transpose(board)
        board, done = cover_up(board)
        board, merged, score = merge(board)
        board = cover_up(board)[0]
        board = transpose(board)
    elif move == 1:  # Left
        board, done = cover_up(board)
        board, merged, score = merge(board)
        board = cover_up(board)[0]
    elif move == 2:  # Right
        board = reverse(board)
        board, done = cover_up(board)
        board, merged, score = merge(board)
        board = cover_up(board)[0]
        board = reverse(board)
    elif move == 3:  # Down
        board = transpose(board)
        board = reverse(board)
        board, done = cover_up(board)
        board, merged, score = merge(board)
        board = cover_up(board)[0]
        board = reverse(board)
        board = transpose(board)
    else:
        print("ILLEGAL MOVE")
        return None, 0

    return board, score

# Main game loop
def main():
    print("NEW GAME")
    board = new_game(4)
    board = add_two(board)
    board = add_two(board)
    score = 0

    print(board)
    print()

    while True:
        move = ''
        while not move.isdigit() or int(move) not in range(4):
            move = input("Enter move (0: Up, 1: Left, 2: Right, 3: Down): ")

        move = int(move)
        board, move_score = perform_move(board, move)
        score += move_score

        if board is None:
            print("Invalid move. Try again.")
            continue

        board = add_two(board)
        print(np.array(board))
        print(f"Score: {score}\n")

        if game_state(board) == 'lose':
            print("YOU LOSE!")
            print("FINAL SCORE:", score)
            break

if __name__ == "__main__":
    main()
 
