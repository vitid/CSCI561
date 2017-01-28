import sys
from copy import copy, deepcopy

class MiniMaxSearch(object):

    def __init__(self,player,depth,board_state):
        self.player = player
        self.max_depth = depth
        self.board_state = board_state
        self.board_processor = BoardProcessor()
        self.logs = []

    @staticmethod
    def compare(a,b):
        """
        Compare 2 numbers, handle Infinity and -Infinity

        :param a:
        :param b:
        :return: 1 -> a>b, 0 -> a==b, -1 -> a<b
        """
        if (type(a) is not str and type(b) is not str):
            if a > b:
                return 1
            elif a < b:
                return -1
            return 0
        if (type(a) is str and type(b) is str):
            if a == b:
                return 0
            if a == "-Infinity":
                return -1
            return 1
        if (type(a) is str):
            if a == "-Infinity":
                return -1
            return 1
        #b is str
        if b == "-Infinity":
            return 1
        return -1

    @staticmethod
    def getMax(a,b):
        if MiniMaxSearch.compare(a,b) == -1:
            return b
        return a

    @staticmethod
    def getMin(a, b):
        if MiniMaxSearch.compare(a, b) == 1:
            return b
        return a

    def getAllPossibleActions(self,current_player,current_board_state):
        """
        Get all legal actions of current_player, according to current_board_state.

        :param current_player:
        :param current_board_state:
        :return: a list of a valid action(which is a placement position) - [(row,column),...], or [] indicates that there is no valid legal move(need to Pass)
        """
        return list(self.board_processor.getAllLegalPlacements(current_player,current_board_state))

    def transition(self,current_player,current_board_state,action):
        """
        Transition function to map f(action) -> state

        :param current_player:
        :param current_board_state:
        :param action: (row,column) to place a chip on, None indicates a Pass Move
        :return: new Board State after applying the action
        """
        #This indicates Pass move
        if(action is None):
            return(deepcopy(current_board_state))

        return self.board_processor.placePosition(current_player,action[0],action[1],current_board_state)

    def getDecision(self):
        """
        Return an action for a particular configuration

        :return: (row,column), a position of cell placement for the player, or None indicates Pass move
        """
        tuple_utility_action = self.maxValue("-Infinity","Infinity", self.player, self.board_state, self.max_depth,None,0)
        return(tuple_utility_action[1])

    def log(self, alpha, beta, depth, placement_position, heuristic_value):
        """
        Collect logs of the search program

        :param alpha:
        :param beta:
        :param depth:
        :param placement_position:
        :param heuristic_value:
        """
        if depth == self.max_depth:
            node_name = "root"
        elif placement_position is None:
            node_name = "pass"
        else:
            node_name = self.board_processor.translateRowColumn(placement_position[0], placement_position[1])

        self.logs.append("{0},{1},{2},{3},{4}".format(node_name,self.max_depth - depth,heuristic_value,alpha,beta))

    def minValue(self,alpha,beta,current_player,current_board_state,depth,parent_action,num_pass):
        """
        Process Minimizer node

        :param alpha:
        :param beta:
        :param current_player:
        :param current_board_state:
        :param depth:
        :param parent_action: (row,column) of a placing cell
        :param num_pass:
        :return: (utility_value,action), action is (row,column) of the placing chip
        """
        #Reach the cut-off level
        if depth <= 0 or num_pass == 2:
            utility_value = self.board_processor.calculateBoardScore(self.player, current_board_state)
            self.log(alpha,beta,depth,parent_action,utility_value)
            return (utility_value,None)

        min_score = "Infinity"
        selected_action = None

        opponent = self.board_processor.getOpponent(current_player)
        actions = self.getAllPossibleActions(current_player,current_board_state)

        #If player unable to make a move
        if (len(actions) == 0):
            actions = [None]
            num_pass = num_pass + 1
        else:
            num_pass = 0

        self.log(alpha, beta, depth, parent_action, min_score)

        for action in actions:
            new_bs = self.transition(current_player,current_board_state,action)
            score = self.maxValue(alpha,beta,opponent,new_bs,depth-1,action,num_pass)[0]
            if MiniMaxSearch.compare(score,min_score) == -1:
                min_score = score
                selected_action = action

            beta_to_update = MiniMaxSearch.getMin(beta,min_score)
            #handle weird grader's logic
            if MiniMaxSearch.compare(beta_to_update,alpha) > 0:
                beta = beta_to_update

            self.log(alpha, beta, depth, parent_action, min_score)

            if MiniMaxSearch.compare(min_score,alpha) <= 0:
                return (min_score, selected_action)

        return(min_score,selected_action)

    def maxValue(self,alpha,beta,current_player,current_board_state,depth,parent_action,num_pass):
        """
        Process Maximizer node

        :param alpha:
        :param beta:
        :param current_player:
        :param current_board_state:
        :param depth:
        :param parent_action:
        :param num_pass
        :return: (utility_value,action), action is (row,column) of the placing chip
        """
        # Reach the cut-off level
        if depth <= 0 or num_pass == 2:
            utility_value = self.board_processor.calculateBoardScore(self.player, current_board_state)
            self.log(alpha, beta, depth, parent_action, utility_value)
            return (utility_value, None)

        max_score = "-Infinity"
        selected_action = None

        opponent = self.board_processor.getOpponent(current_player)
        actions = self.getAllPossibleActions(current_player,current_board_state)

        #If player unable to make a move
        if(len(actions) == 0):
            actions = [None]
            num_pass = num_pass + 1
        else:
            num_pass = 0

        self.log(alpha, beta, depth, parent_action, max_score)

        for action in actions:
            new_bs = self.transition(current_player,current_board_state,action)
            score = self.minValue(alpha,beta,opponent,new_bs,depth-1,action,num_pass)[0]
            if MiniMaxSearch.compare(score,max_score) == 1:
                max_score = score
                selected_action = action

            #handle weird grader's logic
            alpha_to_update = MiniMaxSearch.getMax(alpha,max_score)
            if MiniMaxSearch.compare(alpha_to_update,beta) < 0:
                alpha = alpha_to_update

            self.log(alpha, beta, depth, parent_action, max_score)

            if MiniMaxSearch.compare(max_score,beta) >= 0:
                return (max_score, selected_action)

        return(max_score,selected_action)

class BoardProcessor():
    PLAYER_1 = 'X'
    PLAYER_2 = 'O'
    EMPTY_CELL = '*'

    def __init__(self):
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
        self.cell_weights = [
            [99,-8,8,6,6,8,-8,99],
            [-8,-24,-4,-3,-3,-4,-24,-8],
            [8,-4,7,4,4,7,-4,8],
            [6,-3,4,0,0,4,-3,6],
            [6, -3, 4, 0, 0, 4, -3, 6],
            [8, -4, 7, 4, 4, 7, -4, 8],
            [-8, -24, -4, -3, -3, -4, -24, -8],
            [99, -8, 8, 6, 6, 8, -8, 99]
        ]

    def getOpponent(self,player):
        opponent_player = BoardProcessor.PLAYER_2 if player == BoardProcessor.PLAYER_1 else BoardProcessor.PLAYER_1
        return(opponent_player)

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
        opponent_player = self.getOpponent(player)
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

        opponent_player = self.getOpponent(player)

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

    def calculateBoardScore(self,player,bs):
        """
        Calculate the current board score for a particular player

        :param player:
        :param bs:
        :return:
        """
        opponent_player = self.getOpponent(player)
        flat_weights = [self.cell_weights[i][j] for i in range(0,len(self.cell_weights)) for j in range(0,len(self.cell_weights[0]))]
        flat_boards = [bs[i][j] for i in range(0,len(bs)) for j in range(0,len(bs[0]))]
        tuple_board_weights = zip(flat_boards,flat_weights)
        score = sum([t[1] if t[0] == player else -t[1] if t[0] == opponent_player else 0 for t in tuple_board_weights])
        return(score)

    def translateRowColumn(self,i,j):
        """
        Translate (row,column) to a board representation
        :param i:
        :param j:
        :return: Ex: (0,0) becomes 1a
        """
        return("{1}{0}".format(i+1,chr(65+j).lower()))

if __name__ == '__main__':
    """
    read from the input file

    Ex: python hw1cs561s2017.py -i '/home/vitidn/mydata/repo_git/CSCI561/Assignment_1/instruction/Sample Test Cases/TestCase 3/input.txt'
    """
    player = ""
    max_depth = -1
    board_state = []

    filepath = sys.argv[2]
    f = open(filepath,'r')
    for index,line in enumerate(f):
        line = line.replace("\r","")
        line = line.replace("\n","")
        if(index == 0):
            player = line
        elif(index == 1):
            max_depth = int(line)
        else:
            rows = [c for c in line]
            board_state.append(rows)

    minimax_search = MiniMaxSearch(player,max_depth,board_state)
    select_action = minimax_search.getDecision()
    if(select_action is not None):
        board_processor = BoardProcessor()
        board_state = board_processor.placePosition(player,select_action[0],select_action[1],board_state)
    #print updated board state
    for i in range(0,len(board_state)):
        print("".join([e for e in board_state[i]]))
    #print traversed log
    print("Node,Depth,Value,Alpha,Beta")
    for log in minimax_search.logs:
        print(log)