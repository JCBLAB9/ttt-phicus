import unittest

from flask import json

from app import app
from tictactoe import TicTacToe

game = TicTacToe()


app.testing = True
client = app.test_client()


class TestFlaskRoutes(unittest.TestCase):

    def test_start_game(self):
        response = client.get('/start')
        data = json.loads(response.data)
        self.assertEqual(
            data["board"],
            [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
            )
        self.assertEqual(data["status"], "in progress")
        self.assertEqual(data["current_player"], "X")

    def test_make_move_valid(self):
        client.get('/start')
        response = client.post('/move', json={"row": 1, "col": 1})
        data = json.loads(response.data)
        self.assertEqual(data["result"], "move accepted")
        self.assertEqual(data["board"][1][1], "X")

    def test_make_move_invalid(self):
        client.get('/start')
        response = client.post('/move', json={"row": 3, "col": 3})
        data = json.loads(response.data)
        self.assertEqual(data["result"], "invalid move")

    def test_get_status(self):
        client.get('/start')
        response = client.get('/status')
        data = json.loads(response.data)
        self.assertEqual(
            data["board"],
            [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
            )
        self.assertEqual(data["status"], "in progress")
        self.assertEqual(data["current_player"], "X")


class TestTicTacToe(unittest.TestCase):

    def setUp(self):
        self.game = TicTacToe()

    def test_initialization(self):
        self.assertEqual(
            self.game.display_board(),
            [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
            )
        self.assertEqual(self.game.current_player, 'X')
        self.assertEqual(self.game.status, 'in progress')

    def test_valid_move(self):
        result = self.game.make_move(1, 1)
        self.assertEqual(result, 'move accepted')
        self.assertEqual(self.game.display_board()[1][1], 'X')

    def test_invalid_move(self):
        result = self.game.make_move(3, 3)
        self.assertEqual(result, 'invalid move')
        self.game.make_move(1, 1)
        result = self.game.make_move(1, 1)
        self.assertEqual(result, 'invalid move')

    def test_switch_player(self):
        self.game.make_move(1, 1)
        self.assertEqual(self.game.current_player, 'O')
        self.game.make_move(0, 0)
        self.assertEqual(self.game.current_player, 'X')

    def test_winner(self):
        # X wins
        self.game.make_move(0, 0)  # X
        self.game.make_move(1, 0)  # O
        self.game.make_move(0, 1)  # X
        self.game.make_move(1, 1)  # O
        result = self.game.make_move(0, 2)  # X
        self.assertEqual(result, 'X wins')

    def test_draw(self):
        moves = [
            (0, 0), (0, 1), (0, 2),
            (1, 0), (1, 2), (1, 1),
            (2, 0), (2, 2), (2, 1)
            ]
        for move in moves:
            self.game.make_move(*move)
        self.assertEqual(self.game.status, 'draw')


suite = unittest.TestLoader().loadTestsFromTestCase(TestTicTacToe)
suite2 = unittest.TestLoader().loadTestsFromTestCase(TestFlaskRoutes)
suite.addTest(suite2)
unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    unittest.main()
