from game import *

actions = [0, 1, 2, 3]
train_games = 100
test_games = 30

def convert_to_tuple(arr):
    return tuple(e for e in arr)

class BoardScoreTracker:
    def __init__(self, **args):
        self.board_scores = {}
    
    def get_score(self, board):
        return self.safe_get(board)
    
    def convert_to_tuple(self, arr):
        return tuple(map(tuple, arr))
    
    def safe_get(self, arr):
        key = self.convert_to_tuple(arr)
        return self.board_scores.get(key, 0.0)
    
    def safe_set(self, arr, score):
        key = self.convert_to_tuple(arr)
        self.board_scores[key] = score
    
    def update_score(self, afterstate, score):
        self.safe_set(afterstate, score)

class RowScoreTracker:
    def __init__(self, **args):
        self.rows = [{}, {}, {}, {}]
    
    def get_score(self, board):
        return sum(self.safe_get(row, self.rows[i]) for i, row in enumerate(board))
    
    def safe_get(self, arr, row_dict):
        key = convert_to_tuple(arr)
        return row_dict.get(key, 0.0)
    
    def safe_set(self, arr, score, row_dict):
        key = convert_to_tuple(arr)
        row_dict[key] = score
    
    def update_score(self, afterstate, alpha, reward_next, afterstate_next):
        row_scores = [self.safe_get(row, self.rows[i]) for i, row in enumerate(afterstate)]
        next_rows = [afterstate_next[i] for i in range(4)]
        
        for i in range(4):
            self.safe_set(afterstate[i], sum(row_scores) / 4, self.rows[i])

class TD_AfterState_Agent:
    def __init__(self, **args):
        self.score_tracker = BoardScoreTracker()
        self.learning_rate = 0.0025
    
    def get_move(self, board):
        best_action = None
        max_score = -float('inf')
        for action in actions:
            new_board = perform_move(board, action)[0]
            if np.array_equal(board, new_board): continue
            score = self.evaluate(board, action)
            if score > max_score:
                best_action = action
                max_score = score
        return best_action
    
    def evaluate(self, board, action):
        afterstate, reward_next = perform_move(board, action)
        return self.score_tracker.get_score(afterstate) + reward_next
    
    def update(self, start_state, reward, afterstate, next_state):
        next_action = self.get_move(next_state)
        afterstate_next = next_state
        reward_next = 0
        if next_action:
            afterstate_next, reward_next = perform_move(next_state, next_action)
        score = self.score_tracker.get_score(afterstate) + self.learning_rate * (reward_next + self.score_tracker.get_score(afterstate_next) - self.score_tracker.get_score(afterstate))
        self.score_tracker.update_score(afterstate, score)

def get_highest_tile(board):
    return max(max(row) for row in board)

def run_game(iterations, learning_enabled, agent):
    max_tiles = np.zeros(iterations)
    scores = np.zeros(iterations)
    for i in range(iterations):
        board = new_game(4)
        board = add_two(board)
        board = add_two(board)
        lost = False
        while not lost:
            best_action = agent.get_move(board)
            afterboard, new_score = perform_move(board, best_action)
            scores[i] += new_score
            nextboard = add_two(afterboard)
            
            if learning_enabled:
                agent.update(board, new_score, afterboard, nextboard)
            board = nextboard
            if game_state(board) == 'lose':
                if i % 1000 == 0:
                    print(f"Game {i} score: {scores[i]}")
                max_tiles[i] = get_highest_tile(board)
                lost = True
                continue
    print(f'Scores: {scores}')
    print(f'Max tiles: {max_tiles}')
    print(f'Average score: {scores.mean()}')
    print(f'Standard Deviation of scores: {scores.std()}')
    print('How often agent reached tile:')
    tile = int(max_tiles.max())
    while tile >= 2:
        print(f'{tile}: {np.sum(max_tiles >= tile) / iterations}')
        tile = int(tile / 2)

def main():
    agent = TD_AfterState_Agent()
    
    run_game(train_games, True, agent)
    print()
    run_game(test_games, False, agent)

if __name__ == "__main__":
    main()
