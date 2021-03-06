import unittest
import artificial_intelligence
import game_elements


class TestArtificialIntelligence(unittest.TestCase):
    def setUp(self) -> None:
        self.game_board = game_elements.GameBoard()
        self.player_one = artificial_intelligence.Player(1, self.game_board, vs_ai=True)
        self.player_two = artificial_intelligence.AIPlayer(2, self.game_board)

    def test__check_for_chains_good_inputs(self):
        self.game_board.make_move(0, self.player_one._player_id)
        self.assertListEqual(self.player_two._check_for_chains(5, 0, self.player_two._player_id, self.game_board),
                             [0], msg="Expected [0], got {}".format(self.player_two._check_for_chains(5, 0, self.player_two._player_id, self.game_board)))
        self.assertListEqual(self.player_two._check_for_chains(5, 0, self.player_one._player_id, self.game_board),
                             [1, 1, 1, 1, 1, 1, 1, 1], msg="Expected [1, 1, 1, 1, 1, 1, 1, 1], got {}".format(
                                 self.player_two._check_for_chains(5, 0, self.player_one._player_id, self.game_board)))

    def test__possible_chains_good_inputs(self):
        res = {'own': [
            [[0], [0], [0], [0], [0], [0], [0]],
            [[0], [0], [0], [0], [0], [0], [0]],
            [[0], [0], [0], [0], [0], [0], [0]],
            [[0], [0], [0], [0], [0], [0], [0]],
            [[0], [0], [0], [0], [0], [0], [0]],
            [[0], [0], [0], [0], [0], [0], [0]]
        ],
            'enemy': [
                [[0], [0], [0], [0], [0], [0], [0]],
                [[0], [0], [0], [0], [0], [0], [0]],
                [[0], [0], [0], [0], [0], [0], [0]],
                [[0], [0], [0], [0], [0], [0], [0]],
                [[0], [0], [0], [0], [0], [0], [0]],
                [[1, 1, 1, 1, 1, 1, 1, 1], [0], [0], [0], [0], [0], [0]]
            ]
        }

        self.game_board.make_move(0, self.player_one._player_id)
        self.assertDictEqual(self.player_two._possible_chains(), res, msg="Expected {}, got {}".format(res, self.player_two._possible_chains()))

    def test__choices_good_inputs(self):
        res = {'own': {'0': 1, '1': 1, '2': 1, '3': 1, '4': 1, '5': 1, '6': 1},
               'enemy': {'0': 3, '1': 3, '2': 1, '3': 1, '4': 1, '5': 1, '6': 1}}
        self.game_board.make_move(0, self.player_one._player_id)
        self.assertDictEqual(self.player_two._choices(res), {1: 3, 2: 3, 3: 1.5, 4: 1.5, 5: 1.5, 6: 1.5, 7: 1.5},
                             msg="Expected {}, got {}".format({1: 3, 2: 3, 3: 1.5, 4: 1.5, 5: 1.5, 6: 1.5, 7: 1.5},
                                                               self.player_two._choices(res)))

    def test__simulate_move_good_inputs(self):
        self.game_board.make_move(0, self.player_one._player_id)

        expected_results = {
            'own': [1, 1, 1, 1, 1, 1, 1, 1],
            'enemy': [3, 3, 1, 1, 1, 1, 1]
        }
        for i in range(7):
            self.assertEqual(self.player_two._simulate_move(i, own=True), expected_results['own'][i], msg="Expected {}, got {}".format(expected_results['own'][i], self.player_two._simulate_move(i, own=True)))
            self.assertEqual(self.player_two._simulate_move(i, own=False), expected_results['enemy'][i], msg="Expected {}, got {}".format(expected_results['enemy'][i], self.player_two._simulate_move(i, own=False)))


if __name__ == '__main__':
    unittest.main()
