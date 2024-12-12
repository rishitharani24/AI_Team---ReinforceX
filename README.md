# Reinforcement Learning for Game 2048

## Team Members:
- **Rishitha Rani Pakam**
- **Narasimha Reddy Padire**
- **Sai Teja Somboju**

**Under the Guidance of: Dr. Shivanjali Khare**

---

## Introduction:
2048 is a popular single-player puzzle game where players combine numbered tiles to maximize their score and reach tiles with values like 2048 or higher. While its rules are simple, the game presents a complex challenge due to random tile generation, limited board space, and the need for strategic decision-making. Solving this problem efficiently is important because it involves optimizing gameplay strategies under uncertainty, which is akey challenge in artificial intelligence.

Developing AI agents to play 2048 using reinforcement learning techniques, such as Q-learning and Temporal Difference (TD) Learning, to make smart decisions in uncertain conditions can lead to more effective decision-making. By comparing these methods with others like Expectimax and baseline models, this research not only aims to improve game performance but also demonstrates how such techniques can be applied to real-world problems that require complex decision-making under constraints.

---

## Research Question:
We hypothesize that an AI agent, utilizing reinforcement learning methods like Q-learning and Temporal Difference (TD) learning, can effectively play the game 2048 by selecting optimal moves to maximize the score, achieve tile values of 2048 or higher, and minimize decision time compared to other strategies like Expectimax and baseline approaches.

---
## Requirements
- Python 3.7 or higher
- NumPy library
---
---
## Usage Instructions:
Download all the codes present in this repository and place them in a single folder.

## game.py:
To play the game, navigate to the directory where codes has been saved and run the script in the terminal (python game.py). It initializes a 4x4 grid with two random tiles (2 or 4). Use numeric inputs (0: Up, 1: Left, 2: Right, 3: Down) to slide tiles. After each move, a new tile appears on the grid. The goal is to combine tiles with the same value to create higher-value tiles while maximizing your score. The game ends when no moves are possible, and your final score is displayed.

---
## AI Strategies:
1. **Random Agent** (Baseline Model):
   - **Description**: IT'S A RANDOM AGENT WHICH PERFORMS RANDOM MOVES.
   - **Random Agent Code Usage Instructions**: Open terminal or command prompt and navigate to the directory where you saved MRANDOM.py.Run the script python MRANDOM.py in your terminal. The output will display the average score, standard deviation of scores, and the frequency of reaching different tile values across multiple simulated games.

2. **Q-Learning**:
   - **Description**: Q-Learning is a model-free reinforcement learning algorithm. It enables the AI agent to learn the best actions to take in a given state by updating its Q-values through experience.
   - **Implementation**: In our project, the agent evaluated the after-state of the board after each move. It used a reward system to update its Q-values, focusing on maximizing scores and reaching higher tiles. The balance between exploration (trying new moves) and exploitation (choosing known best moves) was crucial for improvement.
   - **Q-Learning Code Usage Instructions**: Open terminal and navigate to the directory where you saved MQlearning.py and execute it using the command python MQlearning.py. The script trains a reinforcement learning agent to play 2048, evaluates its performance, and displays the average score, standard deviation, and tile frequency for both training and evaluation phases.

3. **TD-Learning**:
   - **Description**: Temporal Difference (TD) Learning is another reinforcement learning method that predicts future rewards dynamically.
   - **Implementation**: Our TD-Learning agent assessed the board state after each move. It predicted the expected future rewards and adjusted scores incrementally using a learning rate, leading to faster convergence compared to Q-Learning. This method allowed the agent to make smarter moves dynamically.
   - **TD-Learning Code Usage Instructions**: Open terminal and navigate to the directory where you saved MTD.py and execute it using the command python MTD.py. The agent will play multiple games, learning from its mistakes and improving its strategy over time. Code will output the average score, standard deviation of scores, and the frequency of reaching different tile values for both training and evaluation phases.

4. **Expectimax**:
   - **Description**: Expectimax is a heuristic search algorithm that alternates between maximizing the player’s move and expecting random tile placements on the board. By evaluating all possible outcomes up to a certain depth, it selects the move with the highest expected value.
   - **Implementation**: Our Expectimax agent recursively evaluated moves using a depth-limited search. For each move, it considered the potential placement of new tiles (2 or 4) and the player’s response, aiming to maximize long-term scores. Depth levels controlled the computational complexity.
   - **Expectimax Code Usage Instructions**: Open terminal and navigate to the directory where you saved expectimax_agent.py and execute it using the command python expectimax_agent.py. Code will train a Minimax agent with alpha-beta pruning to play 2048. The agent will play multiple games, making decisions based on a search tree of possible moves. The results will display the average score, standard deviation of scores, and the frequency of reaching different tile values.

---

## Observed Results:
### Random Agent:
- **Average Score**: 958.71
- **Standard Deviation**: 470.32
- **Success rate for reaching Highest tile**: Rarely reaches higher tiles (e.g., 256,512 or beyond).

### Q-Learning:
- **Average Score**: 2549.54 (after 10,000 games)
- **Standard Deviation**: 1224.46
- **Success rate for reaching Highest tile**: Reaches tile 512 with a frequency of 4.89%.

### TD-Learning:
- **Average Score**: 3394.14 (after 10,000 games)
- **Standard Deviation**: 1658.34
- **Success rate for reaching Highest tile**:
  - Tile 512: 18.91%
  - Tile 1024: 0.04%

### Expectimax:
- **Average Score**: 31,958.4 (at depth 2)
- **Standard Deviation**: 7502.50
- **Success rate for reaching Highest tile**:
  - Tile 2048: 0.8%

- **Average Score**: 40,389.4 (at depth 3)
- **Standard Deviation**: 9328.45
- **Success rate for reaching Highest tile**:
  - Tile 2048: 1.56%

---

## Comparison of Agent Performance:
1. **Random Agent**:
   - Achieves the lowest average score (958.71).
   - Rarely progresses beyond the 256 tile.
2. **Q-Learning**:
   - Moderate performance, showing improvement with training.
   - Requires extensive updates to the Q-table.
3. **TD-Learning**:
   - Outperforms Q-Learning with better consistency and efficiency.
   - Reaches higher tiles like 1024 with proper parameter tuning.
4. **Expectimax**:
   - Best overall performance, frequently reaching 2048 tiles.
   - High computational cost due to depth-limited tree search.

---

## Limitations:
- High time complexity for Expectimax due to tree-based evaluation.
- Dependence on extensive training for Q-Learning and TD-Learning.
- Sensitivity to hyperparameter tuning, such as learning rates.
- Limited applicability of all agents to larger grids or varied game environments.

---

## Future Scope:
1. **Advanced Techniques**: Implement Deep Q-Learning to handle large state spaces.
2. **Optimizations**: Improve Expectimax with pruning and heuristic evaluations.
3. **Generalization**: Adapt agents for larger grids and real-world applications.
4. **Efficiency**: Fine-tune learning rates and parameters for better performance.

---

## Conclusion:
The project demonstrates the effectiveness of AI techniques in solving strategic games like 2048. Among the strategies tested:
- Expectimax delivers the highest performance but is computationally expensive.
- TD-Learning strikes a balance between efficiency and performance.
- Q-Learning requires extensive training but outperforms the Random Agent.
- The Random Agent serves as a baseline with minimal computational cost.

This research highlights trade-offs between learning efficiency, computational complexity, and gameplay performance, offering valuable insights for future AI applications.

---
---
## Project Structure

The project is organized as follows:

- **`main/`**: Contains the core implementation files for the 2048 game AI.
  - **`expectimax_agent.py`**: Python implementation of the Expectimax agent.
  - **`game.py`**: The main game logic for 2048, which is used by all agents.
  - **`MQlearning.py`**: Implementation of the Q-learning algorithm.
  - **`MRANDOM.py`**: Implementation of the random agent.
  - **`MTD.py`**: Implementation of the Temporal Difference (TD) learning algorithm.

  - **`Pseudocodes/`**: Contains pseudocode files describing the algorithms used in the project.
    - **`Expectimax.txt`**: Pseudocode for the Expectimax algorithm.
    - **`Qlearning.txt`**: Pseudocode for the Q-learning algorithm.
    - **`RandomAgent.txt`**: Pseudocode for the Random agent.
    - **`TDLearning.txt`**: Pseudocode for the Temporal Difference (TD) learning algorithm.

  - **`Results.txt`**: Contains the results from the experiments, including scores, success rates, and performance comparisons.

  - **`ReinforceforceX_ProjectProposal.pdf`**: The project proposal document, describing the goals, methodologies, and plan for the project.

  -  **`AI_FINAL_PPT.pptx`**: Final PowerPoint presentation summarizing the project.

  - **`README.md`**: This file, which provides an overview of the project, installation instructions, and usage guidelines.

---

**Thank You!**
