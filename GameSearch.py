class GameSearch:
    def __init__(self, game):
        self.game = game
        self.node_counter = 0
        self.pruned_nodes = 0
        self.search_method = "MM"  # default to minimax

    def minimax(self, state, depth, maximizingPlayer):
        self.node_counter += 1

        if depth == 0 or self.game.is_terminal(state):
            heuristic_value = self.evaluate_state(state)
            return heuristic_value

        if maximizingPlayer:
            maxEval = float('-inf')
            best_move = None
            possible_moves = self.game.get_possible_moves(self.game.max)
            for move in sorted(possible_moves):
                child_state = self.game.apply_move(state, move)
                eval = self.minimax(child_state, depth - 1, False)
                if eval > maxEval:
                    maxEval = eval
                    best_move = move
                elif eval == maxEval and best_move is not None:
                    best_move = self.break_tie(move, best_move)  # add a tie-breaking method here
            if depth == self.game.depth:
                return best_move
            return maxEval
        else:
            minEval = float('inf')
            best_move = None
            possible_moves = self.game.get_possible_moves(self.game.min)
            for move in sorted(possible_moves):
                child_state = self.game.apply_move(state, move)
                eval = self.minimax(child_state, depth - 1, True)
                if eval < minEval:
                    minEval = eval
                    best_move = move
                elif eval == minEval and best_move is not None:
                    best_move = self.break_tie(move, best_move)
            if depth == self.game.depth:
                return best_move
            return minEval

    def alpha_beta_minimax(self, state, depth, maximizingPlayer, alpha=float('-inf'), beta=float('inf')):
        self.node_counter += 1

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
                    best_move = self.break_tie(move, best_move)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    self.pruned_nodes += 1
                    break
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
                    best_move = self.break_tie(move, best_move)
                beta = min(beta, eval)
                if beta <= alpha:
                    self.pruned_nodes += 1
                    break
            return best_move if depth == self.game.depth else minEval

    def print_evaluation_results(self):
        print(f"total nodes evaluated: {self.node_counter}")
        print(f"total nodes pruned: {self.pruned_nodes}")

    def get_possible_moves_sorted(self, state, player):
        possible_moves = self.game.get_possible_moves(player)

        return sorted(possible_moves, key=lambda move: self.evaluate_move(state, move, player),
                      reverse=player == self.game.max)

    def evaluate_move(self, state, move, player):
        temp_state = self.game.apply_move(state, move)

        return self.evaluate_state(temp_state)

    def break_tie(self, move1, move2):
        # prefer moves that reduce manhattan distance
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
            return float('inf')  # max wins
        if min_pos == goal:
            return float('-inf')  # min wins
        max_distance = abs(max_pos[0] - goal[0]) + abs(max_pos[1] - goal[1])
        min_distance = abs(min_pos[0] - goal[0]) + abs(min_pos[1] - goal[1])
        return min_distance - max_distance

    def get_best_move(self, alphaBeta=False):
        self.node_counter = 0

        current_state = self.game.get_current_state()
        maximizingPlayer = self.game.current_player == self.game.max

        if alphaBeta:
            best_move = self.alpha_beta_minimax(current_state, self.game.depth, maximizingPlayer)
        else:
            best_move = self.minimax(current_state, self.game.depth, maximizingPlayer)

        return best_move
