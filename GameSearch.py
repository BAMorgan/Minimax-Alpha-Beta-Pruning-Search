# GameSearch.py
from graphviz import Digraph

class GameSearch:
    def __init__(self, game):
        self.game = game
        self.node_counter = 0
        self.pruned_nodes = 0

    def minimax(self, state, depth, maximizingPlayer):
        if depth == 0 or self.game.is_terminal(state):
            heuristic_value = self.evaluate_state(state)
            return heuristic_value

        if maximizingPlayer:
            maxEval = float('-inf')
            best_move = None
            possible_moves = self.game.get_possible_moves(self.game.max)
            for move in sorted(possible_moves):  # Sorting or prioritizing moves
                child_state = self.game.apply_move(state, move)
                eval = self.minimax(child_state, depth - 1, False)
                if eval > maxEval:
                    maxEval = eval
                    best_move = move
                elif eval == maxEval and best_move is not None:
                    best_move = self.break_tie(move, best_move)  # Add a tie-breaking method here
            if depth == self.game.depth:
                return best_move
            return maxEval
        else:
            minEval = float('inf')
            best_move = None
            possible_moves = self.game.get_possible_moves(self.game.min)
            for move in sorted(possible_moves):  # Sorting or prioritizing moves
                child_state = self.game.apply_move(state, move)
                eval = self.minimax(child_state, depth - 1, True)
                if eval < minEval:
                    minEval = eval
                    best_move = move
                elif eval == minEval and best_move is not None:
                    best_move = self.break_tie(move, best_move)  # Add a tie-breaking method here
            if depth == self.game.depth:
                return best_move
            return minEval

    def alpha_beta_minimax(self, state, depth, maximizingPlayer, alpha=float('-inf'), beta=float('inf')):
        self.node_counter += 1  # Increment the counter for each node evaluated

        if depth == 0 or self.game.is_terminal(state):
            heuristic_value = self.evaluate_state(state)
            return heuristic_value

        best_move = None
        if maximizingPlayer:
            maxEval = float('-inf')
            possible_moves = self.get_possible_moves_sorted(state, self.game.max)
            for move in possible_moves:
                child_state = self.game.apply_move(state, move)
                eval = self.alpha_beta_minimax(child_state, depth - 1, False, alpha, beta)
                if eval > maxEval:
                    maxEval = eval
                    best_move = move
                elif eval == maxEval and best_move is not None:
                    best_move = self.break_tie(move, best_move)  # Add a tie-breaking method here
                alpha = max(alpha, eval)
                if beta <= alpha:
                    self.pruned_nodes += 1  # Increment pruned nodes counter
                    break  # Beta cut-off
            return best_move if depth == self.game.depth else maxEval
        else:
            minEval = float('inf')
            possible_moves = self.get_possible_moves_sorted(state, self.game.min)
            for move in possible_moves:
                child_state = self.game.apply_move(state, move)
                eval = self.alpha_beta_minimax(child_state, depth - 1, True, alpha, beta)
                if eval < minEval:
                    minEval = eval
                    best_move = move
                elif eval == minEval and best_move is not None:
                    best_move = self.break_tie(move, best_move)  # Add a tie-breaking method here
                beta = min(beta, eval)
                if beta <= alpha:
                    self.pruned_nodes += 1  # Increment pruned nodes counter
                    break  # Alpha cut-off
            return best_move if depth == self.game.depth else minEval

    def print_evaluation_results(self):
        print(f"Total nodes evaluated: {self.node_counter}")
        print(f"Total nodes pruned: {self.pruned_nodes}")

    def get_possible_moves_sorted(self, state, player):
        possible_moves = self.game.get_possible_moves(player)
        # Sort moves based on heuristic evaluation, ascending order for MIN, descending for MAX
        print("Player: ", player," Sorted moves: ",sorted(possible_moves, key=lambda move: self.evaluate_move(state, move, player),
                      reverse=player == self.game.max))
        return sorted(possible_moves, key=lambda move: self.evaluate_move(state, move, player),
                      reverse=player == self.game.max)

    def evaluate_move(self, state, move, player):
        # Temporarily apply the move to evaluate its potential
        temp_state = self.game.apply_move(state, move)
        print("Move: ", move, " Value: ", self.evaluate_state(temp_state))

        return self.evaluate_state(temp_state)


    def break_tie(self, move1, move2):
        # Implement a tie-breaking strategy, e.g., prefer moves that reduce Manhattan distance

        if self.manhattan_distance(move1, self.game.goal) < self.manhattan_distance(move2, self.game.goal):
            return move1
        else:
            return move2


    def manhattan_distance(self, move, goal):
        return abs(move[0] - goal[0]) + abs(move[1] - goal[1])

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

    def get_best_move(self, alphaBeta = False):
        current_state = self.game.get_current_state()
        if alphaBeta:
            best_move = self.alpha_beta_minimax(current_state, self.game.depth, False)
        else:
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
        tree.render('game_tree', view=True)
