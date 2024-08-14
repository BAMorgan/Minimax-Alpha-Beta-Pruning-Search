# GameSearch.py
from graphviz import Digraph

class GameSearch:
    def __init__(self, game):
        self.game = game
        self.node_counter = 0
    def manhattan_distance(self, move, goal):
        return abs(move[0] - goal[0]) + abs(move[1] - goal[1])

    def minimax(self, state, depth, maximizingPlayer):
        if depth == 0 or self.game.is_terminal(state):
            heuristic_value = self.evaluate_state(state)
            return heuristic_value

        if maximizingPlayer:
            maxEval = float('-inf')
            best_move = None
            possible_moves = self.game.get_possible_moves(self.game.max)
            for move in possible_moves:
                child_state = self.game.apply_move(state, move)
                eval = self.minimax(child_state, depth - 1, False)
                if eval > maxEval:
                    maxEval = eval
                    best_move = move
            if depth == self.game.depth:
                return best_move  # Ensure we return the best move at the top level
            return maxEval  # Otherwise, return the maxEval for the recursive step
        else:
            minEval = float('inf')
            best_move = None
            possible_moves = self.game.get_possible_moves(self.game.min)
            for move in possible_moves:
                child_state = self.game.apply_move(state, move)
                eval = self.minimax(child_state, depth - 1, True)
                if eval < minEval:
                    minEval = eval
                    best_move = move
                print(f"Evaluating move {move}: minEval={minEval}, best_move={best_move}")
            if depth == self.game.depth:
                return best_move  # Ensure we return the best move at the top level
            return minEval  # Otherwise, return the minEval for the recursive step

    def evaluate_state(self, state):
        max_pos = state['max_position']
        min_pos = state['min_position']
        goal = state['goal']
        if max_pos == goal:
            return float('inf')  # Max wins
        if min_pos == goal:
            return float('-inf')  # Min wins
        max_distance = abs(max_pos[0] - goal[0]) + abs(max_pos[1] - goal[1])
        min_distance = abs(min_pos[0] - goal[0]) + abs(min_pos[1] - goal[1])
        return min_distance - max_distance

    def get_best_move(self):
        current_state = self.game.get_current_state()
        best_move = self.minimax(current_state, self.game.depth, False)
        return best_move

    def generate_tree(self, state, depth, graph=None, parent_node=None):
        if graph is None:
            graph = Digraph()

        node_id = f"node{self.node_counter}"
        self.node_counter += 1

        heuristic_value = self.evaluate_state(state)
        caller = "MIN" if state['current_player'] == self.game.max else "MAX"
        label = f"Max: {state['max_position']}\nMin: {state['min_position']}\nHeuristic: {heuristic_value}\nLast move by: {caller}"

        if state['max_position'] == self.game.goal:
            label += "\nMax Wins!"
        elif state['min_position'] == self.game.goal:
            label += "\nMin Wins!"

        graph.node(node_id, label)

        if parent_node:
            graph.edge(parent_node, node_id)

        if depth == 0 or self.game.is_terminal(state):
            return graph

        current_player = state['current_player']
        possible_moves = self.game.get_possible_moves(current_player)

        for move in possible_moves:
            child_state = self.game.apply_move(state, move)
            self.generate_tree(child_state, depth - 1, graph, node_id)

        return graph

    def visualize_tree(self, state, depth):
        self.node_counter = 0
        tree = self.generate_tree(state, depth)
        tree.render('game_tree', view=True)  # Save and open the tree visualization

