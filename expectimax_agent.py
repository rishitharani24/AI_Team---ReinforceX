from game import *
import numpy as np

class Agent:
    def __init__(self, depth=2):
        self.moves = [0, 1, 2, 3]
        self.depth = depth
        print("Agent initialized with depth:", self.depth)

    def get_move(self, board):
        max_depth = self.depth * 3  # 1 max layer (player), 2 expect layers (2 or 4 and placement)
        value, move = self._maximize(board, 1, max_depth)
        return move

    def _maximize(self, board, current_depth, max_depth):
        if self._is_terminal(board, current_depth, max_depth):
            return self._evaluate(board), None

        value = float('-inf')
        best_move = None

        for move in self.moves:
            new_board = perform_move(board, move)[0]
            if np.array_equal(board, new_board):
                continue  # Skip moves that do nothing
            expected_value, _ = self._expect(new_board, current_depth + 1, max_depth)
            if expected_value > value:
                value, best_move = expected_value, move

        return value, best_move

    def _expect(self, board, current_depth, max_depth):
        empty_cells = get_empty_cells(board)
        if not empty_cells:
            return 0, None

        expected_value = 0
        probability = 1 / len(empty_cells)

        for cell in empty_cells:
            new_value = self._simulate(board, cell, current_depth + 1, max_depth)
            expected_value += probability * new_value

        return expected_value, None

    def _simulate(self, board, cell, current_depth, max_depth):
        board[cell[0]][cell[1]] = 2
        value_with_two, _ = self._maximize(board, current_depth + 1, max_depth)

        board[cell[0]][cell[1]] = 4
        value_with_four, _ = self._maximize(board, current_depth + 1, max_depth)

        board[cell[0]][cell[1]] = 0  # Reset cell
        return 0.9 * value_with_two + 0.1 * value_with_four

    def _evaluate(self, board):
        num_empty = len(get_empty_cells(board))
        merges, horizontal_mono, vertical_mono = self._get_board_metrics(board)

        return (350 * num_empty) + (800 * merges) - (20 * (horizontal_mono + vertical_mono))

    def _get_board_metrics(self, board):
        merges = self._count_merges(board)
        horizontal_mono = self._calculate_monotonicity(board)
        vertical_mono = self._calculate_monotonicity(np.transpose(board))

        return merges, horizontal_mono, vertical_mono

    def _count_merges(self, board):
        merges = 0
        for row in board:
            merges += sum(row[i] == row[i + 1] for i in range(len(row) - 1) if row[i] != 0)
        for col in np.transpose(board):
            merges += sum(col[i] == col[i + 1] for i in range(len(col) - 1) if col[i] != 0)
        return merges

    def _calculate_monotonicity(self, matrix):
        monotonicity = 0
        for row in matrix:
            differences = np.diff(row)
            monotonicity += sum(abs(differences[differences > 0]))
        return monotonicity

    def _is_terminal(self, board, current_depth, max_depth):
        if game_state(board) == 'lose':
            return True
        return current_depth > max_depth

    def get_max_tile(self, board):
        return np.max(board)


def run_game(agent, iterations=5):
    scores = []
    max_tiles = []

    for game_number in range(iterations):
        board = add_two(add_two(new_game(4)))
        print(f"Starting Game {game_number}")
        score = 0

        while game_state(board) != 'lose':
            move = agent.get_move(board)
            if move is None:
                print("No valid move. Board state:")
                print(board)
                break

            board, new_score = perform_move(board, move)
            score += new_score
            board = add_two(board)

        max_tile = agent.get_max_tile(board)
        scores.append(score)
        max_tiles.append(max_tile)

        print(f"Game {game_number} complete. Score: {score}, Max Tile: {max_tile}")

    print_results(scores, max_tiles)


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
        print(f"{max_tile}: {np.sum(max_tiles >= max_tile) / len(max_tiles):.2f}")
        max_tile //= 2


if __name__ == "__main__":
    agent = Agent(depth=1)
    run_game(agent)
