from game import *
import numpy as np

"""
TD Learning with afterstate solution:
- Implements TD learning for afterstates: the state after a move but before a new tile appears.
- Uses row-wise tuples to reduce state space complexity.
"""

possible_moves = [0, 1, 2, 3]
training_games = 10000
evaluation_games = 30


class FullBoardScoreManager:
    """
    Manages scores for the entire board without splitting rows.
    """

    def __init__(self):
        self.score_storage = {}

    def compute_score(self, board):
        """
        Retrieves the score associated with the given board state.
        """
        return self.safe_retrieve(board)

    def convert_to_tuple(self, arr):
        """
        Converts a 2D array to a tuple of tuples.
        """
        return tuple(map(tuple, arr))

    def safe_retrieve(self, arr):
        """
        Safely retrieves the score of a given board state.
        """
        state = self.convert_to_tuple(arr)
        return self.score_storage.get(state, 0.0)

    def safe_store(self, arr, score):
        """
        Safely stores the score for a given board state.
        """
        state = self.convert_to_tuple(arr)
        self.score_storage[state] = score

    def update_score(self, afterstate, score):
        """
        Updates the score of a given afterstate.
        """
        self.safe_store(afterstate, score)


class RowScoreManager:
    """
    Tracks scores for each row independently, treating rows as separate state spaces.
    """

    def __init__(self):
        self.row_scores = [{} for _ in range(4)]

    def compute_score(self, board):
        """
        Computes the total score for the board by summing scores of individual rows.
        """
        return sum(self.safe_retrieve(board[i], self.row_scores[i]) for i in range(4))

    def convert_to_tuple(self, arr):
        """
        Converts an array to a tuple.
        """
        return tuple(arr)

    def safe_retrieve(self, arr, row_dict):
        """
        Safely retrieves the score of a row.
        """
        state = self.convert_to_tuple(arr)
        return row_dict.get(state, 0.0)

    def safe_store(self, arr, score, row_dict):
        """
        Safely stores the score for a row.
        """
        state = self.convert_to_tuple(arr)
        row_dict[state] = score

    def update_score(self, afterstate, score):
        """
        Updates the scores of individual rows proportionally.
        """
        for i in range(4):
            self.safe_store(afterstate[i], score / 4, self.row_scores[i])


class ReinforcementAgent:
    """
    Implements Q-learning for afterstates with score tracking for each move.
    """

    def __init__(self):
        self.scoreTrackers = [FullBoardScoreManager() for _ in range(4)]
        self.learning_rate = 0.0025

    def get_best_move(self, board):
        """
        Evaluates all possible moves and selects the one with the highest score.
        """
        best_move = None
        highest_score = -float('inf')

        for move in possible_moves:
            updated_board = perform_move(board, move)[0]
            if np.array_equal(board, updated_board):
                continue  # Ignore moves that have no effect
            move_score = self.evaluate_action(board, move)
            if move_score > highest_score:
                best_move = move
                highest_score = move_score

        return best_move

    def evaluate_action(self, board, action):
        """
        Retrieves the score for a specific action on the given board.
        """
        return self.scoreTrackers[action].compute_score(board)

    def update_policy(self, current_state, action, reward, next_state):
        """
        Implements TD learning: V(s) ← V(s) + α(r + V(s') − V(s)).
        """
        next_action = self.get_best_move(next_state)
        next_value = 0
        if next_action is not None:
            next_value = self.evaluate_action(next_state, next_action)

        current_score = self.scoreTrackers[action].compute_score(current_state)
        updated_score = current_score + self.learning_rate * (reward + next_value - current_score)
        self.scoreTrackers[action].update_score(current_state, updated_score)


def find_highest_tile(board):
    """
    Finds the maximum tile on the board.
    """
    return max(max(row) for row in board)


def simulate_game(num_iterations, training_mode, agent):
    """
    Simulates the game for a given number of iterations.
    """
    max_tiles = np.zeros(num_iterations)
    scores = np.zeros(num_iterations)

    for i in range(num_iterations):
        board = new_game(4)
        board = add_two(board)
        board = add_two(board)

        while game_state(board) != 'lose':
            action = agent.get_best_move(board)
            post_move_board, reward = perform_move(board, action)
            scores[i] += reward
            next_board = add_two(post_move_board)

            if training_mode:
                agent.update_policy(board, action, reward, next_board)

            board = next_board

        max_tiles[i] = find_highest_tile(board)

        if i % 1000 == 0:
            print(f"Game {i} Score: {scores[i]}")

    print(f"Average Score: {scores.mean()}, Standard Deviation: {scores.std()}")
    print("Tile Reach Frequency:")
    tile = int(max_tiles.max())
    while tile >= 2:
        print(f"{tile}: {np.sum(max_tiles >= tile) / num_iterations}")
        tile //= 2


def main():
    agent = ReinforcementAgent()
    simulate_game(training_games, True, agent)
    print("\nEvaluation Phase:")
    simulate_game(evaluation_games, False, agent)


if __name__ == "__main__":
    main()
