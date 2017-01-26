from copy import copy, deepcopy

PLAYER_1 = 'X'
PLAYER_2 = 'O'
EMPTY_CELL = '*'

board_state = [
                ['*','*','*','*','*','*','*','*'],
                ['*','*','*','*','*','*','*','*'],
                ['*','*','*','*','*','*','*','*'],
                ['*','*','*','*','*','*','*','*'],
                ['*','*','*','*','*','*','*','*'],
                ['*','*','*','*','*','*','*','*'],
                ['*','*','*','*','*','*','*','*'],
                ['*','*','*','*','*','*','*','*']
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
    if(bs[i][j] != EMPTY_CELL):
        return False
    opponent_player = PLAYER_2 if player == PLAYER_1 else PLAYER_1
    #count (#player,#opponent_player) for all possible directions
    #define a set of direction to probe
    directions = [
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
    for example: (-1,-1) means diagonal left downward

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

for i in range(0,8):
   for j in range(0,8):
       print(str(i) + "," + str(j) + ":" + str(isPositionLegal(PLAYER_1,i,j,board_state)) )