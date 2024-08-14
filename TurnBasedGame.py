# TurnBasedGame.py
import random
from GameSearch import GameSearch
from pyamaze import maze, agent, textLabel, COLOR

class TurnBasedGame:
    def __init__(self):
        self.rows = 10
        self.cols = 10
        self.maze = maze(self.rows, self.cols)
        self.maze.CreateMaze(random.randint(1, self.cols), random.randint(1, self.rows), loopPercent=100,
                             theme=COLOR.dark)

        self.max = agent(self.maze, random.randint(1, self.cols), random.randint(1, self.rows), shape='arrow',
                         footprints=True, color=COLOR.red)
        self.min = agent(self.maze, random.randint(1, self.cols), random.randint(1, self.rows), shape='arrow',
                         footprints=True, color=COLOR.blue)
        self.goal = self.maze.getGoal()
        self.current_player = self.max
        self.turn_label = textLabel(self.maze, "Turn", "Max")

        self.depth = 2  # Depth for the minimax algorithm
        self.game_search = GameSearch(self)

        self.enable_turn_based_control()

    def set_manual_state(self, max_position, min_position, goal_position):
        """Manually set the positions for testing."""
        self.max.position = max_position
        self.min.position = min_position
        self.goal = goal_position
        self.current_player = self.min  # You can change this to Min if needed

    def update_game_tree(self):
        current_state = self.get_current_state()
        self.game_search.visualize_tree(current_state, self.depth)

    def get_current_state(self):
        return {
            'max_position': self.max.position,
            'min_position': self.min.position,
            'goal': self.goal,
            'current_player': self.current_player
        }

    def is_terminal(self, state):
        return state['max_position'] == self.goal or state['min_position'] == self.goal

    def apply_move(self, state, move):
        new_state = state.copy()
        if state['current_player'] == self.max:
            new_state['max_position'] = move
            new_state['current_player'] = self.min
        else:
            new_state['min_position'] = move
            new_state['current_player'] = self.max
        return new_state

    def switch_player(self):
        if self.current_player == self.max:
            self.current_player = self.min
            self.turn_label.value = "Min"

            self.update_game_tree()  # Update and print the game tree after each move
            self.ai_move()  # Trigger AI move immediately after switching to min
        else:
            self.current_player = self.max
            self.turn_label.value = "Max"


    def move_current_player(self, direction):
        if direction == 'Left':
            self.current_player.moveLeft(None)
        elif direction == 'Right':
            self.current_player.moveRight(None)
        elif direction == 'Up':
            self.current_player.moveUp(None)
        elif direction == 'Down':
            self.current_player.moveDown(None)

        if self.current_player.position == self.goal:
            self.turn_label.value = f"{self.current_player.color.name.capitalize()} Wins!"
            self.maze._win.unbind('<Left>')
            self.maze._win.unbind('<Right>')
            self.maze._win.unbind('<Up>')
            self.maze._win.unbind('<Down>')
            return

        # Visualize the tree after MAX moves
        if self.current_player == self.max:
            self.update_game_tree()  # Update and visualize the game tree

        self.switch_player()

    def get_possible_moves(self, agent):
        neighbors = []
        x, y = agent.position
        if self.maze.maze_map[(x, y)]['E']:
            neighbors.append((x, y + 1))
        if self.maze.maze_map[(x, y)]['W']:
            neighbors.append((x, y - 1))
        if self.maze.maze_map[(x, y)]['N']:
            neighbors.append((x - 1, y))
        if self.maze.maze_map[(x, y)]['S']:
            neighbors.append((x + 1, y))
        return neighbors

    def ai_move(self):
        best_move = self.game_search.get_best_move()
        if best_move:
            self.apply_move_to_agent(self.min, best_move)

        if self.min.position == self.goal:
            self.turn_label.value = f"{self.min.color.name.capitalize()} Wins!"
            self.maze._win.unbind('<Left>')
            self.maze._win.unbind('<Right>')
            self.maze._win.unbind('<Up>')
            self.maze._win.unbind('<Down>')
            return

        self.switch_player()

    def apply_move_to_agent(self, agent, move):
        if move[0] > agent.x:
            agent.moveDown(None)
        elif move[0] < agent.x:
            agent.moveUp(None)
        elif move[1] > agent.y:
            agent.moveRight(None)
        elif move[1] < agent.y:
            agent.moveLeft(None)

    def enable_turn_based_control(self):
        def move_left(event):
            self.move_current_player('Left')

        def move_right(event):
            self.move_current_player('Right')

        def move_up(event):
            self.move_current_player('Up')

        def move_down(event):
            self.move_current_player('Down')

        self.maze._win.bind('<Left>', move_left)
        self.maze._win.bind('<Right>', move_right)
        self.maze._win.bind('<Up>', move_up)
        self.maze._win.bind('<Down>', move_down)

    def run(self):
        self.maze.run()

def main():
    game = TurnBasedGame()
    game.run()



    # # Initialize the maze without running the GUI
    # rows, cols = 10, 10
    # test_maze = maze(rows, cols)
    # test_maze.CreateMaze(random.randint(1, 10), random.randint(1, 10),loopPercent=100, theme=COLOR.light)  # Create a maze with some loops
    #
    # # Manually create agents (this does not require GUI)
    # max_agent = agent(test_maze, x=8, y=1, shape='arrow', color=COLOR.red)
    # min_agent = agent(test_maze, x=4, y=7, shape='arrow', color=COLOR.blue)
    # goal_position = test_maze.getGoal()
    #
    # # Initialize the TurnBasedGame with these agents
    # game = TurnBasedGame()
    # game.max = max_agent
    # game.min = min_agent
    # game.goal = goal_position
    #
    # # Set manual state to test
    # game.set_manual_state((random.randint(1,10), random.randint(1,10)), (random.randint(1,10), random.randint(1,10)), goal_position)
    #
    # # Initialize GameSearch
    # game_search = GameSearch(game)
    #
    #
    # # Test the current state and heuristic
    # current_state = game.get_current_state()
    # print("Current State:", current_state)
    # print("Possible moves:", game.get_possible_moves(min_agent))
    # game_search.visualize_tree(current_state, game.depth)
    # heuristic = game_search.evaluate_state(current_state)
    # print("Heuristic Value:", heuristic)
    #
    # # Test the minimax function
    # best_move = game_search.minimax(current_state, 2, False)  # Min's turn
    # print("Best Move for Min:", best_move)
    #
    # # Apply the best move and print the new state
    # new_state = game.apply_move(current_state, best_move)
    # print("New State after Min's move:", new_state)

if __name__ == "__main__":
    main()