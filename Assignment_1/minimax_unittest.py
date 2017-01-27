from hw1cs561s2017 import BoardProcessor
import unittest

class MiniMaxSearch(object):

    def __init__(self,player,depth,board_state):
        self.player = player
        self.depth = depth
        self.board_state = board_state
        self.board_processor = BoardProcessor()

    def getAllPossibleActions(self,current_player,current_board_state):
        """

        :param current_player:
        :param current_board_state:
        :return: a list of a valid action(which is a placement position) - [(row,column),...]
        """
        return list(self.board_processor.getAllLegalPlacements(current_player,current_board_state))

    def transition(self,current_player,current_board_state,action):
        """
        Transition function to map f(action) -> state

        :param current_player:
        :param current_board_state:
        :param action: (row,column) to place a chip on
        :return: new Board State after applying the action
        """
        return self.board_processor.placePosition(current_player,action[0],action[1],current_board_state)

    def getDecision(self):
        """
        Return an action for a particular configuration

        :return: (row,column), a position of cell placement for the player
        """
        opponent = self.board_processor.getOpponent(self.player)
        max_score = "-Infinity"
        selected_action = None
        for action in self.getAllPossibleActions(self.player,self.board_state):
            new_bs = self.transition(self.player,self.board_state,action)
            score = self.minValue(opponent,new_bs,self.depth - 1)
            if max_score == "-Infinity" or score > max_score:
                max_score = score
                selected_action = action
        return(selected_action)

    def minValue(self,current_player,current_board_state,depth):
        #Reach the cut-off level
        if depth <= 0:
            return (self.board_processor.calculateBoardScore(current_player, current_board_state))

        min_score = "Infinity"
        opponent = self.board_processor.getOpponent(current_player)
        actions = self.getAllPossibleActions(current_player,current_board_state)

        #If player unable to make a move
        if(len(actions) == 0):
            opponent_actions = self.getAllPossibleActions(opponent,current_board_state)
            #Opponent also unable to make a move
            if(len(opponent_actions)==0):
                #Terminal state where niether player can move
                return(self.board_processor.calculateBoardScore(current_player,current_board_state))
            else:
                #Opponent can still make a move, wait for instruction on how to handle this...
                pass

        for action in actions:
            new_bs = self.transition(current_player,current_board_state,action)
            score = self.maxValue(opponent,new_bs,depth-1)
            if min_score == "Infinity" or score < min_score:
                min_score = score

        return(min_score)

    def maxValue(self,current_player,current_board_state,depth):
        #Reach the cut-off level
        if depth <= 0:
            return (self.board_processor.calculateBoardScore(current_player, current_board_state))

        max_score = "-Infinity"
        opponent = self.board_processor.getOpponent(current_player)
        actions = self.getAllPossibleActions(current_player,current_board_state)

        #If player unable to make a move
        if(len(actions) == 0):
            opponent_actions = self.getAllPossibleActions(opponent,current_board_state)
            #Opponent also unable to make a move
            if(len(opponent_actions)==0):
                #Terminal state where niether player can move
                return(self.board_processor.calculateBoardScore(current_player,current_board_state))
            else:
                #Opponent can still make a move, wait for instruction on how to handle this...
                pass

        for action in actions:
            new_bs = self.transition(current_player,current_board_state,action)
            score = self.minValue(opponent,new_bs,depth-1)
            if max_score == "-Infinity" or score > max_score:
                max_score = score

        return(max_score)

class TestMiniMaxSearch(unittest.TestCase):
    def setUp(self):
        self.board_processor = BoardProcessor()

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