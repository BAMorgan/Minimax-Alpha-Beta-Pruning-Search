import unittest
from GameSearch import GameSearch
from MazeRunner import TurnBasedGame

class TestMinimax(unittest.TestCase):

    def setUp(self):
        # Set up a controlled game environment for testing
        self.game = TurnBasedGame()
        self.game_search = GameSearch(self.game)

        # Manually set the initial positions for Max and Min for controlled tests
        self.game.max.position = (5, 3)
        self.game.min.position = (2, 5)
        self.game.goal = (1, 1)

        # Disable any random elements for reproducibility
        self.game.depth = 3  # Set the depth for the minimax algorithm

    def test_minimax_terminal_state(self):
        # Test a terminal state where Max wins
        state = {
            'max_position': (1, 1),
            'min_position': (2, 5),
            'goal': (1, 1),
            'current_player': self.game.max
        }
        result = self.game_search.minimax(state, self.game.depth, True)
        self.assertEqual(result, float('inf'))  # Max should win, so result should be positive infinity

    def test_minimax_non_terminal_state(self):
        # Test a non-terminal state where the AI has to choose a move
        state = {
            'max_position': (8, 1),
            'min_position': (4, 7),
            'goal': (1, 1),
            'current_player': self.game.min
        }
        best_move = self.game_search.minimax(state, self.game.depth, False)
        self.assertIn(best_move, [(4, 6), (5,7)])  # The best moves should be one of these based on the heuristic

    def test_evaluate_state(self):
        # Test the evaluation function separately
        state = {
            'max_position': (8, 1),
            'min_position': (4, 7),
            'goal': (1, 1),
            'current_player': self.game.min
        }
        heuristic = self.game_search.evaluate_state(state)
        self.assertEqual(heuristic, 3)  # Expected heuristic value for this state

if __name__ == '__main__':
    unittest.main()
