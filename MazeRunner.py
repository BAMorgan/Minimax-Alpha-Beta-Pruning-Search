import random, sys
from GameSearch import GameSearch
from pyamaze import maze, agent, textLabel, COLOR

class TurnBasedGame:
    def __init__(self, size):
        if size == 10:
            self.rows = 10
            self.cols = 10
        elif size == 20:
            self.rows = 20
            self.cols = 30

        self.maze = maze(self.rows, self.cols)
        self.maze.CreateMaze(random.randint(1, self.rows), random.randint(1, self.cols), loopPercent=100,
                             theme=COLOR.dark)

        max_x = random.randint(1, self.rows)
        max_y = random.randint(1, self.cols)
        self.max = agent(self.maze, max_x, max_y, shape='arrow', footprints=True, color=COLOR.red)

        min_x = random.randint(1, self.rows)
        min_y = random.randint(1, self.cols)
        self.min = agent(self.maze, min_x, min_y, shape='arrow', footprints=True, color=COLOR.blue)

        self.goal = self.maze.getGoal()
        self.current_player = self.max  # default to max, will be set by MazeRunner

        self.depth = 5  # depth for the minimax algorithm
        self.game_search = GameSearch(self)
        self.game_search.search_method = "MM"  # default to minimax

        self.human_player = None
        self.turn_label = textLabel(self.maze, "Turn", "Max's Turn")

        self.control_instructions = textLabel(self.maze, "Controls", "use wasd or arrow keys to move")

        self.enable_turn_based_control()

    def set_manual_state(self, max_position, min_position, goal_position):
        """manually set the positions for testing."""
        self.max.position = max_position
        self.min.position = min_position
        self.goal = goal_position
        self.current_player = self.min  # you can change this to min if needed

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

    def set_human_player(self, player):
        """sets which player is controlled by the human."""
        if player == 1:
            self.human_player = self.max
        else:
            self.human_player = self.min

    def switch_player(self):
        if self.current_player == self.max:
            self.current_player = self.min
            self.turn_label.value = "min's turn"
            next_player_name = "min"
        else:
            self.current_player = self.max
            self.turn_label.value = "max's turn"
            next_player_name = "max"

        if self.current_player == self.human_player:
            print(f"it is {next_player_name}'s turn.")
        else:
            print(f"it is {next_player_name}'s turn.")
            self.ai_move()

    def move_current_player(self, direction):
        initial_position = self.current_player.position

        if direction == 'left':
            self.current_player.moveLeft(None)
        elif direction == 'right':
            self.current_player.moveRight(None)
        elif direction == 'up':
            self.current_player.moveUp(None)
        elif direction == 'down':
            self.current_player.moveDown(None)

        if self.current_player.position != initial_position:
            current_player_name = "MAX" if self.current_player == self.max else "MIN"
            print(f"{current_player_name} (human) moved: {self.current_player.position}")

        if self.current_player.position == self.goal:
            self.turn_label.value = f"{self.current_player.color.name.capitalize()} Wins!"
            if self.current_player == self.human_player:
                print("Human beats AI!")
            else:
                print("AI beats Human!")
            self.maze._win.unbind('<Left>')
            self.maze._win.unbind('<Right>')
            self.maze._win.unbind('<Up>')
            self.maze._win.unbind('<Down>')
            return

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
        best_move = self.game_search.get_best_move(alphaBeta=self.game_search.search_method == "AB")
        if best_move:
            current_player_name = "MAX" if self.current_player == self.max else "MIN"
            self.apply_move_to_agent(self.current_player, best_move)

            print(f"{current_player_name} (AI) moved: {best_move}")

        if self.current_player.position == self.goal:
            self.turn_label.value = f"{self.current_player.color.name.capitalize()} Wins!"
            if self.current_player == self.human_player:
                print("Human beats AI!")
            else:
                print("AI beats Human!")
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
            if self.current_player == self.human_player:
                self.move_current_player('Left')

        def move_right(event):
            if self.current_player == self.human_player:
                self.move_current_player('Right')

        def move_up(event):
            if self.current_player == self.human_player:
                self.move_current_player('Up')

        def move_down(event):
            if self.current_player == self.human_player:
                self.move_current_player('Down')

        self.maze._win.bind('<Left>', move_left)
        self.maze._win.bind('<Right>', move_right)
        self.maze._win.bind('<Up>', move_up)
        self.maze._win.bind('<Down>', move_down)

        self.maze._win.bind('a', move_left)
        self.maze._win.bind('d', move_right)
        self.maze._win.bind('w', move_up)
        self.maze._win.bind('s', move_down)

    def run(self):
        self.maze.run()

def main():
    if len(sys.argv) != 4:
        print("Usage: MazeRunner.py [player] [searchmethod] [size]")
        print("Example: MazeRunner.py 1 MM 10")

        sys.exit(1)

    player = int(sys.argv[1])
    searchmethod = sys.argv[2]
    size = int(sys.argv[3])

    if player not in [1, 2] or searchmethod not in ['MM', 'AB'] or size not in [10, 20]:
        print("Invalid input arguments.")
        print("MazeRunner.py [player] [searchmethod] [size]")
        sys.exit(1)

    game = TurnBasedGame(size)

    if player == 1:
        game.set_human_player(1)
        game.current_player = game.max
    else:
        game.set_human_player(2)
        game.current_player = game.min

    game.game_search.search_method = searchmethod


    print("WASD or arrow keys to move!")
    game.run()

if __name__ == "__main__":
    main()
