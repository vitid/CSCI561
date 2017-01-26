from copy import copy, deepcopy
import unittest

PLAYER_1 = 'X'
PLAYER_2 = 'O'
EMPTY_CELL = '*'
directions = directions = [
        #left
        (0,-1),
        #right
        (0,1),
        #up
        (-1,0),
        #down
        (1,0),
        #diagonal
        #up-left
        (-1,-1),
        #up-right
        (-1,1),
        #down-left
        (1,-1),
        #down-right
        (1,1)

    ]

def isPositionLegal(player,i,j,bs):
    """
    Check whether to current position is legal or not

    :param player: PLAYER_1 or PLAYER_2
    :param i: row number, 0-7
    :param j: column number, 0-7
    :param bs: Board State
    :return: True/False, is the position legal or not
    """
    global directions
    if(bs[i][j] != EMPTY_CELL):
        return False
    opponent_player = PLAYER_2 if player == PLAYER_1 else PLAYER_1
    #count (#player,#opponent_player) for all possible directions
    for direction in directions:
        count_tuple = probeBoard(direction[0],direction[1],i+direction[0],j+direction[1],player,opponent_player,bs)
        #at least 1 opponent is circumscribed by the player
        if(count_tuple[0] == 1 and count_tuple[1] > 0):
            return True
    return False

def probeBoard(direction_i,direction_j,i,j,player,opponent_player,bs):
    """
    Supplement function to recursively collect a counter and check whether the position is valid or not

    (direction_i,direction_j) indicates which direction to go
    for example: (-1,-1) means diagonal left-up

    return (#player,#opponent_player) collected so far

    :param direction_i: -1/0/1
    :param direction_j: -1/0/1
    :param i:
    :param j:
    :param player:
    :param opponent_player:
    :param bs: Board State
    :return: (#player,#opponent_player) collected so far
    """
    if(i<0 or i>7 or j<0 or j>7):
        return (0,0)
    if(bs[i][j] == EMPTY_CELL):
        return (0,0)
    if(bs[i][j] == player):
        return (1,0)
    count_tuple = probeBoard(direction_i, direction_j, i + direction_i, j + direction_j, player, opponent_player, bs)
    return (count_tuple[0],count_tuple[1]+1)

def placePosition(player,i,j,bs):
    """
    Place a chip on the position (i,j). Flip opponent's chip(s) appropriately.
    (Board State returned is a new instance)

    :param player:
    :param i:
    :param j:
    :param bs:
    :return: Board State after the chip's placement
    """
    global directions
    result_bs = deepcopy(bs)

    opponent_player = PLAYER_2 if player == PLAYER_1 else PLAYER_1

    #collect the flipped cells in a temp list so it doesn't mess up the whole board processing
    flip_list = []
    for direction in directions:
        count_tuple = probeBoard(direction[0],direction[1],i+direction[0],j+direction[1],player,opponent_player,bs)
        #at least 1 opponent is circumscribed by the player
        if(count_tuple[0] == 1 and count_tuple[1] > 0):
            flip_i = i + direction[0]
            flip_j = j + direction[1]
            for k in range(0,count_tuple[1]):
                flip_list.append((flip_i,flip_j))
                flip_i += direction[0]
                flip_j += direction[1]
    #place on the current cell
    result_bs[i][j] = player
    #flip cells appropriately
    for flip_cell in flip_list:
        result_bs[flip_cell[0]][flip_cell[1]] = player
    return(result_bs)

class TestBoard(unittest.TestCase):
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
                self.assertFalse(isPositionLegal(PLAYER_1, i, j, board_state))
                self.assertFalse(isPositionLegal(PLAYER_2, i, j, board_state))

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
                    self.assertTrue(isPositionLegal(PLAYER_1, i, j, board_state))
                else:
                    self.assertFalse(isPositionLegal(PLAYER_1, i, j, board_state))
                if (i,j) in valid_player_2_positions:
                    self.assertTrue(isPositionLegal(PLAYER_2, i, j, board_state))
                else:
                    self.assertFalse(isPositionLegal(PLAYER_2, i, j, board_state))

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
        self.assertEqual(placePosition(PLAYER_1,1,3,board_state),expected_board_state_p_1)
        self.assertEqual(placePosition(PLAYER_2, 4, 3, board_state), expected_board_state_p_2)

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
        self.assertEqual(placePosition(PLAYER_1,3,4,board_state),expected_board_state_p_1)
        self.assertEqual(placePosition(PLAYER_2, 2, 2, board_state), expected_board_state_p_2)


if __name__ == '__main__':
    unittest.main()