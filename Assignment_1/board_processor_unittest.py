from hw1cs561s2017 import BoardProcessor
import unittest

class TestBoardProcessor(unittest.TestCase):
    def setUp(self):
        self.board_processor = BoardProcessor()

    def test_isPositionLegal_0(self):
        board_state = [
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*']
        ]
        for i in range(0, 8):
            for j in range(0, 8):
                self.assertFalse(self.board_processor.isPositionLegal(BoardProcessor.PLAYER_1, i, j, board_state))
                self.assertFalse(self.board_processor.isPositionLegal(BoardProcessor.PLAYER_2, i, j, board_state))

    def test_isPositionLegal_1(self):
        board_state = [
            ['*', '*', '*', '*', '*', '*', 'O', 'X'],
            ['*', '*', '*', '*', '*', '*', 'O', 'O'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['X', 'X', 'X', '*', '*', '*', '*', '*'],
            ['O', 'O', 'X', '*', '*', '*', '*', '*'],
            ['O', 'O', 'X', '*', '*', '*', '*', '*']
        ]
        valid_player_1_positions = [(0,5),(2,5),(2,7)]
        valid_player_2_positions = [(4,0),(4,1),(4,2),(4,3),(5,3),(6,3),(7,3)]
        for i in range(0, 8):
            for j in range(0, 8):
                if (i,j) in valid_player_1_positions:
                    self.assertTrue(self.board_processor.isPositionLegal(BoardProcessor.PLAYER_1, i, j, board_state))
                else:
                    self.assertFalse(self.board_processor.isPositionLegal(BoardProcessor.PLAYER_1, i, j, board_state))
                if (i,j) in valid_player_2_positions:
                    self.assertTrue(self.board_processor.isPositionLegal(BoardProcessor.PLAYER_2, i, j, board_state))
                else:
                    self.assertFalse(self.board_processor.isPositionLegal(BoardProcessor.PLAYER_2, i, j, board_state))

    def test_placePosition_0(self):
        board_state = [
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', 'O', '*', '*', '*', '*'],
            ['*', '*', '*', 'X', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*']
        ]
        expected_board_state_p_1 = [
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', 'X', '*', '*', '*', '*'],
            ['*', '*', '*', 'X', '*', '*', '*', '*'],
            ['*', '*', '*', 'X', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*']
        ]
        expected_board_state_p_2 = [
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', 'O', '*', '*', '*', '*'],
            ['*', '*', '*', 'O', '*', '*', '*', '*'],
            ['*', '*', '*', 'O', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*']
        ]
        self.assertEqual(self.board_processor.placePosition(BoardProcessor.PLAYER_1,1,3,board_state),expected_board_state_p_1)
        self.assertEqual(self.board_processor.placePosition(BoardProcessor.PLAYER_2, 4, 3, board_state), expected_board_state_p_2)

    def test_placePosition_1(self):
        board_state = [
            ['*', '*', 'O', '*', '*', '*', '*', '*'],
            ['*', '*', 'X', 'O', 'X', '*', '*', '*'],
            ['*', '*', '*', 'O', 'O', 'O', '*', '*'],
            ['*', 'X', 'O', 'O', '*', '*', '*', '*'],
            ['*', '*', '*', 'X', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*']
        ]
        expected_board_state_p_1 = [
            ['*', '*', 'O', '*', '*', '*', '*', '*'],
            ['*', '*', 'X', 'O', 'X', '*', '*', '*'],
            ['*', '*', '*', 'X', 'X', 'O', '*', '*'],
            ['*', 'X', 'X', 'X', 'X', '*', '*', '*'],
            ['*', '*', '*', 'X', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*']
        ]
        expected_board_state_p_2 = [
            ['*', '*', 'O', '*', '*', '*', '*', '*'],
            ['*', '*', 'O', 'O', 'X', '*', '*', '*'],
            ['*', '*', 'O', 'O', 'O', 'O', '*', '*'],
            ['*', 'X', 'O', 'O', '*', '*', '*', '*'],
            ['*', '*', '*', 'X', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*']
        ]
        self.assertEqual(self.board_processor.placePosition(BoardProcessor.PLAYER_1,3,4,board_state),expected_board_state_p_1)
        self.assertEqual(self.board_processor.placePosition(BoardProcessor.PLAYER_2, 2, 2, board_state), expected_board_state_p_2)

    def test_getAllLegalPlacements(self):
        board_state = [
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', 'O', '*', '*', '*', '*', '*', '*'],
            ['*', '*', 'X', '*', '*', '*', '*', '*'],
            ['*', '*', 'X', '*', '*', '*', '*', '*'],
            ['*', '*', 'X', 'O', '*', '*', '*', '*'],
            ['*', '*', '*', 'O', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*']
        ]
        self.assertEqual(list(self.board_processor.getAllLegalPlacements(BoardProcessor.PLAYER_1,board_state)),[(0,0),(4,4),(5,4),(6,4)])
        self.assertEqual(list(self.board_processor.getAllLegalPlacements(BoardProcessor.PLAYER_2, board_state)), [(2,1),(3,1),(3,3),(4,1)])

    def test_calculateBoardScore_0(self):
        board_state = [
            ['O', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', 'O', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', 'X', '*', '*', '*', '*'],
            ['*', '*', '*', 'X', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*']
        ]
        self.assertEqual(self.board_processor.calculateBoardScore(BoardProcessor.PLAYER_1,board_state),-98)
        self.assertEqual(self.board_processor.calculateBoardScore(BoardProcessor.PLAYER_2, board_state), 98)
    def test_translateRowColumn(self):
        self.assertEqual(self.board_processor.translateRowColumn(0,0),"a1")
        self.assertEqual(self.board_processor.translateRowColumn(0, 7), "h1")
        self.assertEqual(self.board_processor.translateRowColumn(4, 4), "e5")
        self.assertEqual(self.board_processor.translateRowColumn(7, 0), "a8")
        self.assertEqual(self.board_processor.translateRowColumn(7, 7), "h8")
if __name__ == '__main__':
    unittest.main()