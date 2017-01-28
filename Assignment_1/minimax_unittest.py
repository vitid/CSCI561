from hw1cs561s2017 import MiniMaxSearch, BoardProcessor
import unittest

class TestMiniMaxSearch(unittest.TestCase):
    def setUp(self):
        self.board_processor = BoardProcessor()

    def test_compare(self):
        self.assertEqual(MiniMaxSearch.compare(0,0),0)
        self.assertEqual(MiniMaxSearch.compare(10, 0), 1)
        self.assertEqual(MiniMaxSearch.compare(-10, 0), -1)
        self.assertEqual(MiniMaxSearch.compare("Infinity", "-Infinity"), 1)
        self.assertEqual(MiniMaxSearch.compare("-Infinity", "Infinity"), -1)
        self.assertEqual(MiniMaxSearch.compare("-Infinity", "-Infinity"), 0)
        self.assertEqual(MiniMaxSearch.compare("-Infinity", -10), -1)
        self.assertEqual(MiniMaxSearch.compare("Infinity", -10), 1)
        self.assertEqual(MiniMaxSearch.compare(-10,"-Infinity"), 1)
        self.assertEqual(MiniMaxSearch.compare(-10,"Infinity"), -1)

    def test_getMin(self):
        self.assertEqual(MiniMaxSearch.getMin(10,-10), -10)
        self.assertEqual(MiniMaxSearch.getMin(1,"Infinity"),1)
        self.assertEqual(MiniMaxSearch.getMin("Infinity",1), 1)
        self.assertEqual(MiniMaxSearch.getMin(1, "-Infinity"), "-Infinity")
        self.assertEqual(MiniMaxSearch.getMin("-Infinity", 1), "-Infinity")

    def test_getMax(self):
        self.assertEqual(MiniMaxSearch.getMax(10,-10), 10)
        self.assertEqual(MiniMaxSearch.getMax(1,"Infinity"),"Infinity")
        self.assertEqual(MiniMaxSearch.getMax("Infinity",1), "Infinity")
        self.assertEqual(MiniMaxSearch.getMax(1, "-Infinity"), 1)
        self.assertEqual(MiniMaxSearch.getMax("-Infinity", 1), 1)

    def test_search_0(self):
        board_state = [
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', 'O', 'X', '*', '*', '*'],
            ['*', '*', '*', 'X', 'O', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*']
        ]
        expected_board_state = [
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', 'X', '*', '*', '*', '*'],
            ['*', '*', '*', 'X', 'X', '*', '*', '*'],
            ['*', '*', '*', 'X', 'O', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*']
        ]
        minimax_searcher = MiniMaxSearch(BoardProcessor.PLAYER_1,2,board_state)
        action = minimax_searcher.getDecision()
        actual_board_state = self.board_processor.placePosition(BoardProcessor.PLAYER_1,action[0],action[1],board_state)
        self.assertEqual(actual_board_state,expected_board_state)

    def test_search_1(self):
        board_state = [
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', 'O', 'X', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*']
        ]
        expected_board_state = [
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', 'X', 'X', 'X', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*']
        ]
        minimax_searcher = MiniMaxSearch(BoardProcessor.PLAYER_1,3,board_state)
        action = minimax_searcher.getDecision()
        actual_board_state = self.board_processor.placePosition(BoardProcessor.PLAYER_1,action[0],action[1],board_state)
        self.assertEqual(actual_board_state,expected_board_state)

    def test_search_2(self):
        board_state = [
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', 'X', 'X', '*', '*', '*'],
            ['*', '*', '*', '*', 'X', 'X', '*', '*'],
            ['*', '*', '*', 'X', 'X', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*']
        ]
        minimax_searcher = MiniMaxSearch(BoardProcessor.PLAYER_1,3,board_state)
        action = minimax_searcher.getDecision()
        self.assertEqual(action,None)

    def test_search_3(self):
        board_state = [
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', 'X', 'X', 'X', '*', '*'],
            ['*', '*', '*', 'X', 'O', 'X', '*', '*'],
            ['*', '*', '*', 'X', 'X', 'X', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*']
        ]
        minimax_searcher = MiniMaxSearch(BoardProcessor.PLAYER_1,3,board_state)
        action = minimax_searcher.getDecision()
        self.assertEqual(action,None)

    def test_search_4(self):
        board_state = [
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', 'O', '*', '*', '*', 'O', '*', '*'],
            ['X', 'X', 'X', 'X', 'X', 'X', '*', '*']
        ]
        expected_board_state = [
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['*', '*', '*', '*', '*', '*', '*', '*'],
            ['X', '*', '*', '*', '*', '*', '*', '*'],
            ['*', 'X', '*', '*', '*', 'O', '*', '*'],
            ['X', 'X', 'X', 'X', 'X', 'X', '*', '*']
        ]
        minimax_searcher = MiniMaxSearch(BoardProcessor.PLAYER_1,3,board_state)
        action = minimax_searcher.getDecision()
        actual_board_state = self.board_processor.placePosition(BoardProcessor.PLAYER_1,action[0],action[1],board_state)
        self.assertEqual(actual_board_state,expected_board_state)

    def test_search_5(self):
        board_state = [
            ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
            ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
            ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
            ['O', 'O', 'O', 'O', 'O', 'O', 'O', '*'],
            ['O', 'O', 'O', 'O', 'O', 'O', '*', '*'],
            ['O', 'O', 'O', 'O', 'O', 'O', '*', 'X'],
            ['O', 'O', 'O', 'O', 'O', 'O', 'O', '*'],
            ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']
        ]
        minimax_searcher = MiniMaxSearch(BoardProcessor.PLAYER_1,3,board_state)
        action = minimax_searcher.getDecision()
        self.assertEqual(action,None)

if __name__ == '__main__':
    unittest.main()