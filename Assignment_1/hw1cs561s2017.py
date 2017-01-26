from copy import copy, deepcopy

class BoardProcessor():
    def __init__(self):
        self.PLAYER_1 = 'X'
        self.PLAYER_2 = 'O'
        self.EMPTY_CELL = '*'
        self.directions = [
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

    def getAllLegalPlacements(self,player,bs):
        """
        Get all legal cell places for a particular player. This must go from left -> right & top -> bottom

        :param player:
        :param bs: Board State
        :return: (row,col) of all legal placement states
        """
        for i in range(0,8):
            for j in range(0,8):
                if self.isPositionLegal(player,i,j,bs):
                    yield (i,j)

    def isPositionLegal(self,player,i,j,bs):
        """
        Check whether to current position is legal or not

        :param player: PLAYER_1 or PLAYER_2
        :param i: row number, 0-7
        :param j: column number, 0-7
        :param bs: Board State
        :return: True/False, is the position legal or not
        """
        if(bs[i][j] != self.EMPTY_CELL):
            return False
        opponent_player = self.PLAYER_2 if player == self.PLAYER_1 else self.PLAYER_1
        #count (#player,#opponent_player) for all possible directions
        for direction in self.directions:
            count_tuple = self.probeBoard(direction[0],direction[1],i+direction[0],j+direction[1],player,opponent_player,bs)
            #at least 1 opponent is circumscribed by the player
            if(count_tuple[0] == 1 and count_tuple[1] > 0):
                return True
        return False

    def probeBoard(self,direction_i,direction_j,i,j,player,opponent_player,bs):
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
        if(bs[i][j] == self.EMPTY_CELL):
            return (0,0)
        if(bs[i][j] == player):
            return (1,0)
        count_tuple = self.probeBoard(direction_i, direction_j, i + direction_i, j + direction_j, player, opponent_player, bs)
        return (count_tuple[0],count_tuple[1]+1)

    def placePosition(self,player,i,j,bs):
        """
        Place a chip on the position (i,j). Flip opponent's chip(s) appropriately.
        (Board State returned is a new instance)

        :param player:
        :param i:
        :param j:
        :param bs:
        :return: Board State after the chip's placement
        """
        result_bs = deepcopy(bs)

        opponent_player = self.PLAYER_2 if player == self.PLAYER_1 else self.PLAYER_1

        #collect the flipped cells in a temp list so it doesn't mess up the whole board processing
        flip_list = []
        for direction in self.directions:
            count_tuple = self.probeBoard(direction[0],direction[1],i+direction[0],j+direction[1],player,opponent_player,bs)
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