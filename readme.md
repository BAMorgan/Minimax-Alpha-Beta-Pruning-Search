# Grid/Maze Search with Minimax annd Alpha-Beta Pruning

## Overview
This project implements a **Maze Chase game** where an **AI player (MAX)** competes against a **human player (MIN)** to reach a randomly placed goal in a **10×10** or **20×30** maze. The AI uses **Minimax and Alpha-Beta Pruning** to determine the best moves. The game supports **GUI visualization**, **console interactions**, and game statistics tracking.

## Features
- Supports **10×10** and **20×30** maze sizes  
- Implements **Minimax (MM)** and **Alpha-Beta Pruning (AB)** search algorithms  
- **Turn-based gameplay** with AI vs. Human interactions  
- **AI move calculation and pruning optimizations**  
- **Console outputs AI decisions and game results**  
- **GUI visualization of the players' movements**  

## Usage
Run the program with the following command:
```sh
python MazeRunner.py [player] [searchmethod] [size]
```
**Example:**
```sh
python MazeRunner.py 1 MM 10
```
- **player** = 1 (AI plays as MAX) or 2 (AI plays as MIN)  
- **searchmethod** = MM (Minimax) or AB (Alpha-Beta Pruning)  
- **size** = 10 (10×10 maze) or 20 (20×30 maze)  

### Game Moves
- Human inputs their move via the console.  
- AI calculates the best move using Minimax/Alpha-Beta Pruning.  
- The game continues until a player reaches the goal.  

## Requirements
- Python 3.x  
- Required libraries: `random`, `pygame`, `queue`, `pyamaze`  

## Outputs
1. **GUI Output**: Visualizes AI and human movements on the maze.  
2. **Console Output**: Displays AI moves and winner announcements.  
3. **Readme.txt Output**: Includes evaluation function formula and algorithm performance stats.  
