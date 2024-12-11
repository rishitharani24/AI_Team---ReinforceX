from game import * 
import numpy as np

class Agent:
    def __init__(self, depth=2):
        # Initialize the agent with a default search depth
        self.moves = [0, 1, 2, 3]  # Possible moves: up, down, left, right
        self.depth = depth  # Depth of the search tree
        print("Agent initialized with depth:", self.depth)

    def get_move(self, board):
        # Determine the best move for the current board state
        max_depth = self.depth * 3  
        value, move = self._maximize(board, 1, max_depth)  # Maximize the evaluation function
        return move

    def _maximize(self, board, current_depth, max_depth):
        # Maximize the evaluation score for the board
        if self._is_terminal(board, current_depth, max_depth):
            return self._evaluate(board), None  # Terminal condition, evaluate board

        value = float('-inf') 
        best_move = None  # No best move initially

        for move in self.moves:
            # Simulate each move
            new_board = perform_move(board, move)[0]  # Get new board state
            if np.array_equal(board, new_board):
                continue  # Skip invalid moves

            expected_value, _ = self._expect(new_board, current_depth + 1, max_depth)  # Expectimax evaluation
            if expected_value > value:
                value, best_move = expected_value, move  # Update best move and value

        return value, best_move

    def _expect(self, board, current_depth, max_depth):
        # Evaluate expected value for the board considering random tile placements
        empty_cells = get_empty_cells(board)  # Get empty cell positions
        if not empty_cells:
            return 0, None  # No empty cells, return 0

        expected_value = 0
        probability = 1 / len(empty_cells)  # Equal probability for each empty cell

        for cell in empty_cells:
            # Simulate placing tiles (2 or 4) in empty cells
            new_value = self._simulate(board, cell, current_depth + 1, max_depth)
            expected_value += probability * new_value

        return expected_value, None

    def _simulate(self, board, cell, current_depth, max_depth):
        # Simulate placing tiles and evaluate board state
        board[cell[0]][cell[1]] = 2  # Placing 2
        value_with_two, _ = self._maximize(board, current_depth + 1, max_depth)  # Evaluate with 2

        board[cell[0]][cell[1]] = 4  # Placing 4
        value_with_four, _ = self._maximize(board, current_depth + 1, max_depth)  # Evaluate with 4

        board[cell[0]][cell[1]] = 0 
        return 0.9 * value_with_two + 0.1 * value_with_four  # Weighted average for tile probabilities

    def _evaluate(self, board):
        # Evaluate the board based on game-specific heuristics
        num_empty = len(get_empty_cells(board))  # Count empty cells
        merges, horizontal_mono, vertical_mono = self._get_board_metrics(board)  # Board metrics

        # Weighted sum of metrics to evaluate the board
        return (350 * num_empty) + (800 * merges) - (20 * (horizontal_mono + vertical_mono))

    def _get_board_metrics(self, board):
        # Calculate board metrics: merges and monotonicity
        merges = self._count_merges(board)  # Count possible merges
        horizontal_mono = self._calculate_monotonicity(board)  # Horizontal monotonicity
        vertical_mono = self._calculate_monotonicity(np.transpose(board))  # Vertical monotonicity

        return merges, horizontal_mono, vertical_mono

    def _count_merges(self, board):
        # Count adjacent tiles that can be merged
        merges = 0
        for row in board:
            merges += sum(row[i] == row[i + 1] for i in range(len(row) - 1) if row[i] != 0)
        for col in np.transpose(board):
            merges += sum(col[i] == col[i + 1] for i in range(len(col) - 1) if col[i] != 0)
        return merges

    def _calculate_monotonicity(self, matrix):
        # Calculate monotonicity score for rows/columns
        monotonicity = 0
        for row in matrix:
            differences = np.diff(row)  # Calculate differences between adjacent tiles
            monotonicity += sum(abs(differences[differences > 0]))  # Penalize increases
        return monotonicity

    def _is_terminal(self, board, current_depth, max_depth):
        # Check if the board state is terminal
        if game_state(board) == 'lose':
            return True  # Game over
        return current_depth > max_depth  # Exceeded search depth

    def get_max_tile(self, board):
        # Return the maximum tile value on the board
        return np.max(board)


def run_game(agent, iterations=5):
    # Run multiple games with the agent
    scores = []  # List of scores for all games
    max_tiles = []  # List of max tiles for all games

    for game_number in range(iterations):
        board = add_two(add_two(new_game(4)))  # Initialize a new game board
        print(f"Starting Game {game_number}")
        score = 0

        while game_state(board) != 'lose':
            move = agent.get_move(board)  # Get agent's move
            if move is None:
                print("No valid move. Board state:")
                print(board)
                break

            board, new_score = perform_move(board, move)
            score += new_score  # Update score
            board = add_two(board)  # Add a new tile to the board

        max_tile = agent.get_max_tile(board)  # Get the maximum tile achieved
        scores.append(score)  # Store the score
        max_tiles.append(max_tile)  # Store the max tile

        print(f"Game {game_number} complete. Score: {score}, Max Tile: {max_tile}")

    print_results(scores, max_tiles)  # Print the results of all games


def print_results(scores, max_tiles):
    scores = np.array(scores)
    max_tiles = np.array(max_tiles)

    print(f"Scores: {scores}")
    print(f"Max tiles: {max_tiles}")
    print(f"Average score: {scores.mean()}")
    print(f"Standard Deviation of scores: {scores.std()}")

    print("Tile reach statistics:")
    max_tile = int(max_tiles.max())
    while max_tile >= 2:
        print(f"{max_tile}: {np.sum(max_tiles >= max_tile) / len(max_tiles):.2f}")  # Percentage of games reaching each tile
        max_tile //= 2


if __name__ == "__main__":
    agent = Agent(depth=2)  # Initialize agent with a depth of 2
    run_game(agent)  # Run the game with the agent
