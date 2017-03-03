import sys
import copy
import itertools
import random

class PropositionSymbol(object):
    def __init__(self,symbol):

        if len(symbol) == 0:
            raise Exception("PropositionSymbol should not be Empty")

        self.symbol = symbol

    def __eq__(self, other):
        if not isinstance(other,self.__class__):
            return False
        return self.symbol == other.symbol

    def __hash__(self):
        return hash(self.symbol)

class Literal(object):
    def __init__(self,propositionSymbol,isPositive=True):
        self.propositionSymbol = propositionSymbol
        self.isPositive = isPositive
    def isPositiveLiteral(self):
        return self.isPositive

    def isNegativeLiteral(self):
        return not self.isPositive

    def __eq__(self,other):
        if not isinstance(other,self.__class__):
            return False
        return self.propositionSymbol == other.propositionSymbol and self.isPositive == other.isPositive

    def __hash__(self):
        return hash(self.propositionSymbol.symbol + "," + str(self.isPositive))

class Clause(object):
    """
    A disjunction of literals
    """
    def __init__(self,literals):
        self.literals = set(literals) # type: set[Literal]
        self._hash = -1
        self._positiveSymbols = None
        self._negativeSymbols = None
        self._isTautology = None
        self._representation = None

    def getLiterals(self):
        """
        :rtype: set[Literal]
        """
        return self.literals

    def isUnitClause(self):
        return self.getNumberLiterals() == 1

    def getNumberLiterals(self):
        return len(self.literals)

    def isEmpty(self):
        return self.getNumberLiterals() == 0

    def getSymbols(self):
        return self.getPositiveSymbols().union(self.getNegativeSymbols())

    def getPositiveSymbols(self):
        if self._positiveSymbols is None:
            self._positiveSymbols = self._retrievePosOrNeg(True)

        return self._positiveSymbols

    def getNegativeSymbols(self):
        if self._negativeSymbols is None:
            self._negativeSymbols = self._retrievePosOrNeg(False)

        return self._negativeSymbols

    def isTautology(self):
        if self._isTautology is None:
            self._isTautology = len(self.getPositiveSymbols().intersection(self.getNegativeSymbols())) > 0

        return self._isTautology

    def getClauseRepresentation(self):
        """
        :rtype: str

        :return:
        """
        if self._representation is not None:
            return self._representation

        tokens = list()

        for l in self.literals: # type: Literal
            prefix = ""
            if l.isNegativeLiteral():
                prefix = "~"
            tokens.append(prefix + l.propositionSymbol.symbol)

        tokens.sort()
        self._representation = ",".join(tokens)
        return self._representation

    def _retrievePosOrNeg(self,isFetchPositive):
        result = set()
        for e in self.literals:
            if isFetchPositive and e.isPositiveLiteral():
                result.add(e.propositionSymbol)
            elif not isFetchPositive and e.isNegativeLiteral():
                result.add(e.propositionSymbol)
        return result

    def __eq__(self,other):
        if not isinstance(other,self.__class__):
            return False
        return self.literals == other.literals

    def __hash__(self):
        if self._hash > -1:
            return self._hash

        self._hash = hash(self.getClauseRepresentation())

        return self._hash

class PropositionSymbolFactory(object):
    def __init__(self):
        self._ps_dict = {} # type: dict[str,PropositionSymbol]

    def getPropositionSymbol(self,symbol):
        """
        :type symbol: str
        :rtype: PropositionSymbol

        :param symbol:
        :return:
        """

        if symbol not in self._ps_dict:
            self._ps_dict[symbol] = PropositionSymbol(symbol)

        return self._ps_dict[symbol]

class ClauseHelper(object):
    def __init__(self,propositionSymbolFactory):
        self.propositionSymbolFactory = propositionSymbolFactory # type: PropositionSymbolFactory

    def getLiteral(self,token):
        """
        :rtype: Literal

        :param token:
        :return:
        """
        isPositive = True
        if token.startswith("~"):
            token = token[1:]
            isPositive = False
        return Literal(self.propositionSymbolFactory.getPropositionSymbol(token),isPositive)

    def generateClause(self,tokens):
        """
        :type tokens: list[str]
        :rtype: Clause

        :param tokens:
        :return:
        """
        literals = [] # list[Literal]
        for token in tokens:
            literals.append(self.getLiteral(token))

        return Clause(literals)

class DPLL(object):
    """
    Check satisfiability with DPLL algorithm
    """
    def dpllSatisfiable(self,clause_set):
        symbols = list() #type: list[PropositionSymbol]
        for c in clause_set: #type: Clause
            for symbol in c.getSymbols():
                if symbol not in symbols:
                    symbols.append(symbol)
        return self.dpll(clause_set,symbols,Model())

    def dpll(self,clause_set,symbols,model):

        if self.everyClauseTrue(clause_set,model):
            return True

        if self.someClauseFalse(clause_set,model):
            return False

        pAndValue = self.findPureSymbol(symbols,clause_set,model)
        if pAndValue is not None:
            copy_symbols = copy.copy(symbols)
            copy_symbols.remove(pAndValue[0])
            return self.dpll(clause_set,copy_symbols,
                             model.union(pAndValue[0],pAndValue[1]))

        pAndValue = self.findUnitClause(clause_set,model)
        if pAndValue is not None:
            copy_symbols = copy.copy(symbols)
            copy_symbols.remove(pAndValue[0])
            return self.dpll(clause_set, copy_symbols,
                             model.union(pAndValue[0], pAndValue[1]))

        p = symbols[0] #type: PropositionSymbol
        rest = symbols[1:] #type: list[PropositionSymbol]

        return self.dpll(clause_set,rest,model.union(p,True)) or self.dpll(clause_set,rest,model.union(p,False))

    def everyClauseTrue(self,clauses,model):
        return model.satisfies(clauses)

    def someClauseFalse(self,clauses,model):
        for c in clauses:
            v = model.determineValue(c)
            if v is not None and v is False:
                return True
        return False

    def findPureSymbol(self,symbols,clauses,model):
        """
        :type symbols: list[PropositionSymbol]
        :type clauses: set[Clause]
        :type model: Model

        :rtype: (PropositionSymbol,bool)
        """
        result = None
        candidatePurePositiveSymbols = set()
        candidatePureNegativeSymbols = set()
        for c in clauses: #type: Clause
            if model.determineValue(c):
                continue

            for p in c.getPositiveSymbols():
                if p in symbols:
                    candidatePurePositiveSymbols.add(p)

            for p in c.getNegativeSymbols():
                if p in symbols:
                    candidatePureNegativeSymbols.add(p)

        for p in symbols:
            if p in candidatePurePositiveSymbols and p in candidatePureNegativeSymbols:
                candidatePurePositiveSymbols.remove(p)
                candidatePureNegativeSymbols.remove(p)

        if len(candidatePurePositiveSymbols) > 0:
            result = (list(candidatePurePositiveSymbols)[0],True)
        elif len(candidatePureNegativeSymbols) > 0:
            result = (list(candidatePureNegativeSymbols)[0],False)

        return result

    def findUnitClause(self,clauses,model):
        """
        :type clauses: set[Clause]
        :type model: Model

        :rtype: (PropositionSymbol,bool)
        """
        result = None

        for c in clauses: #type: Clause
            if model.determineValue(c) is None:
                unassigned = None #type: Literal
                if c.isUnitClause():
                    unassigned = list(c.getLiterals())[0]
                else:
                    for l in list(c.getLiterals()):
                        value = model.assignments.get(l.propositionSymbol)
                        if value is None:
                            if unassigned is None:
                                unassigned = l
                            else:
                                unassigned = None
                                break

                if unassigned is not None:
                    result = (unassigned.propositionSymbol,unassigned.isPositiveLiteral())
                    break

        return result

class PLResolution(object):
    """
    Modified PLResolution algorithm to just check whether the received CNF are satisfiable or not
    """
    def plResolution(self,clause_set):
        """
        :type clause_set: set[Clause]
        :rtype: bool

        :param clause_set: set of clauses - {Clause,Clause,...}, all are in CNF
        """
        clauses = copy.copy(clause_set) # type: set[Clause]

        empty_clause = Clause([])

        while True:

            new_clauses = set()
            for pair in itertools.combinations(list(clauses),2):
                ci = pair[0] # type: Clause
                cj = pair[1] # type: Clause

                resolvents = self.plResolve(ci,cj)

                if empty_clause in resolvents:
                    return False

                new_clauses = new_clauses.union(resolvents)

            if new_clauses.issubset(clauses):
                return True

            clauses = clauses.union(new_clauses)

    def plResolve(self,ci,cj):
        """
        :rtype: set[Clause]
        :param ci:
        :param cj:
        :return:
        """
        resolvents = set() # type: set[Clause]

        self.resolveTwoClauses(ci, cj, resolvents)
        return resolvents

    def resolveTwoClauses(self, c1, c2, resolvents):
        """
        @type c2: Clause
        @type c1: Clause

        :param c1:
        :param c2:
        :param resolvents:
        :return:
        """
        complementary = c1.getPositiveSymbols().intersection(c2.getNegativeSymbols())
        complementary2 = c2.getPositiveSymbols().intersection(c1.getNegativeSymbols())
        # avoid unnecessary operation
        if len(complementary) > 0 and len(complementary2) > 0:
            # the whole thing will be Tautology
            return

        for complement in complementary: # type: PropositionSymbol
            resolventLiterals = [] # type: list[Literal]
            for c1l in c1.literals: # type: Literal
                if c1l.isNegativeLiteral() or c1l.propositionSymbol != complement:
                    resolventLiterals.append(c1l)
            for c2l in c2.literals: # type: Literal
                if c2l.isPositiveLiteral() or c2l.propositionSymbol != complement:
                    resolventLiterals.append(c2l)

            resolvent = Clause(resolventLiterals)
            if not resolvent.isTautology():
                resolvents.add(resolvent)

        for complement in complementary2: # type: PropositionSymbol
            resolventLiterals = [] # type: list[Literal]
            for c2l in c2.literals: # type: Literal
                if c2l.isNegativeLiteral() or c2l.propositionSymbol != complement:
                    resolventLiterals.append(c2l)
            for c1l in c1.literals: # type: Literal
                if c1l.isPositiveLiteral() or c1l.propositionSymbol != complement:
                    resolventLiterals.append(c1l)

            resolvent = Clause(resolventLiterals)
            if not resolvent.isTautology():
                resolvents.add(resolvent)

class KnowledgeOperator(object):
    def __init__(self,m,n,friend_pairs,enemy_pairs,clauseHelper = ClauseHelper(PropositionSymbolFactory())):
        """
        :type friend_pairs: list[(int,int)]
        :type enemy_pairs: list[(int,int)]

        :param m:
        :param n:
        :param friend_pairs:
        :param enemy_pairs:
        :param clauseHelper:
        """
        self.num_person = m # type: int
        self.num_table = n # type: int
        self.friend_pairs = friend_pairs
        self.enemy_pairs = enemy_pairs
        self.clauseHelper = clauseHelper # type: ClauseHelper

    def getAssociatedClauses(self):
        """
        :rtype: set[Clause]

        :return:
        """
        return self.getClausesOnePersonAtOneTable().union(self.getClausesFriend()).union(self.getClausesEnemy())

    def getClausesOnePersonAtOneTable(self):
        """
        :rtype: set[Clause]

        :return:
        """
        result = set()
        for person_index in range(1,self.num_person+1):
            clause_literals = ["X[{},{}]".format(person_index,table_index) for table_index in range(1,self.num_table + 1)]
            result.add(self.clauseHelper.generateClause(clause_literals))

        table_indexs = range(1,self.num_table+1)

        for person_index in range(1, self.num_person + 1):
            for pair in itertools.combinations(table_indexs,2):
                clause_literals = ["~X[{},{}]".format(person_index,pair[0]),"~X[{},{}]".format(person_index,pair[1])]
                result.add(self.clauseHelper.generateClause(clause_literals))
        return result

    def getClausesFriend(self):
        """
        :rtype: set[Clause]
        :return:
        """
        result = set()
        for person_i,person_j in self.friend_pairs:
            for table_index in range(1,self.num_table + 1):
                result.add(self.clauseHelper.generateClause(["~X[{},{}]".format(person_i,table_index),"X[{},{}]".format(person_j,table_index)]))
                result.add(self.clauseHelper.generateClause(["X[{},{}]".format(person_i, table_index), "~X[{},{}]".format(person_j, table_index)]))
        return result

    def getClausesEnemy(self):
        """
        :rtype: set[Clause]

        :return:
        """
        result = set()
        for person_i,person_j in self.enemy_pairs:
            for table_index in range(1,self.num_table + 1):
                clause_literals = ["~X[{},{}]".format(person_i, table_index), "~X[{},{}]".format(person_j, table_index)]
                result.add(self.clauseHelper.generateClause(clause_literals))
        return result

class Model(object):

    def __init__(self,d={}):
        self.assignments = copy.copy(d) # type:{PropositionSymbol:bool}

    def determineValue(self,c):
        """
        :type c: Clause
        :rtype: bool

        :param c:
        :return:
        """
        # should not happen
        if c.isEmpty():
            raise(Exception("try to determine truth value of and empty clause"))

        if c.isTautology():
            return True

        result = None
        unassignedSymbols = False
        value = None
        for p in c.getPositiveSymbols():
            value = self.assignments.get(p)
            if value is not None:
                if value:
                    result = True
                    break
            else:
                unassignedSymbols = True
        if result is None:
            for p in c.getNegativeSymbols():
                value = self.assignments.get(p)
                if value is not None:
                    if not value:
                        result = True
                        break
                else:
                    unassignedSymbols = True

            if result is None:
                if not unassignedSymbols:
                    result = False

        return result

    def satisfies(self,clauses):
        """
        :type clauses: set[Clause]
        :rtype: bool

        :param clauses:
        :return:
        """
        for c in clauses:
            if not self.determineValue(c):
                return False

        return True

    def flip(self,p):
        """
        :type p: PropositionSymbol

        :rtype: Model
        """
        if p not in self.assignments:
            return self

        if self.assignments[p]:
            return self.union(p,False)
        return self.union(p,True)

    def union(self,p,isTrue):
        """
        :type p: PropositionSymbol
        :type isTrue: bool
        :rtype: Model

        :param p:
        :param isTrue:
        :return:
        """
        m = Model(self.assignments)
        m.assignments[p] = isTrue
        return m

class WalkSAT(object):
    def __init__(self,seed=-1):
        if seed > -1:
            random.seed(seed)

    def walkSAT(self,clauses,p=0.5,maxFlips=10000):
        """
        :type clauses: set[Clause]
        :type p: decimal
        :type maxFlips: int
        :rtype: Model

        :param clauses:
        :param p:
        :param maxFlips:
        :return:
        """
        model = self.randomAssignmentToSymbolsInClauses(clauses)
        for i in range(0,maxFlips):
            if model.satisfies(clauses):
                return model

            clause = self.randomlySelectFalseClause(clauses,model)

            if random.random() < p:
                model = model.flip(self.randomlySelectSymbolFromClause(clause))
            else:
                model = self.flipSymbolInClauseMaximizesNumberSatisfiedClauses(clause,clauses,model)
        return None


    def flipSymbolInClauseMaximizesNumberSatisfiedClauses(self,clause,clauses,model):
        """
        :type clause: Clause
        :type clauses: set[Clause]
        :type model: Model
        """
        result = model

        symbols = clause.getSymbols()
        maxClausesSatisfied = -1
        for symbol in symbols:
            flippedModel = result.flip(symbol)
            numberClausesSatisfied = 0
            for c in clauses:
                if flippedModel.determineValue(c):
                    numberClausesSatisfied += 1

            if numberClausesSatisfied > maxClausesSatisfied:
                result = flippedModel
                maxClausesSatisfied = numberClausesSatisfied
                if numberClausesSatisfied == len(clauses):
                    break
        return result

    def randomlySelectSymbolFromClause(self,clause):
        return random.choice(list(clause.getSymbols()))

    def randomlySelectFalseClause(self,clauses,model):
        """
        :rtype: Clause
        """
        falseClauses = []
        for c in clauses: #type: Clause
            if not model.determineValue(c):
                falseClauses.append(c)

        return random.choice(falseClauses)

    def randomAssignmentToSymbolsInClauses(self,clauses):
        """
        :type clauses: set[Clause]

        :param clauses:
        :return:
        """
        symbols = set() # type: set[PropositionSymbol]
        for c in clauses: # type: Clause
            symbols = symbols.union(c.getSymbols())

        values = {} # type: dict[PropositionSymbol: bool]
        for p in symbols:
            values[p] = random.choice([True, False])

        return Model(values)

if __name__ == "__main__":
    """
    read from the input file

    Ex: python hw2cs561s2017.py'
    """
    num_person = -1
    num_table = -1
    friend_pairs = [] # type:list[tuple[int,int]]
    enemy_pairs = [] # type:list[tuple[int,int]]
    output_content = ""
    isUseDPLL = True

    # parse all arguments from a file
    f = open("input.txt", 'r')
    for index, line in enumerate(f):
        line = line.replace("\r", "")
        line = line.replace("\n", "") # type: str
        if index == 0:
            num_person = int(line.split(" ")[0])
            num_table = int(line.split(" ")[1])
        else:
            person_i = int(line.split(" ")[0])
            person_j = int(line.split(" ")[1])
            relationship = line.split(" ")[2] # can be only F or E
            if relationship == "F":
                friend_pairs.append((person_i,person_j))
            else:
                enemy_pairs.append((person_i,person_j))

    # start PLResolution/ DPLL
    propositionSymbolFactory = PropositionSymbolFactory()
    clauseHelper = ClauseHelper(propositionSymbolFactory)
    knowledgeOperator = KnowledgeOperator(num_person,num_table,friend_pairs,enemy_pairs,clauseHelper)
    clauses = knowledgeOperator.getAssociatedClauses()

    if isUseDPLL:
        dpll = DPLL()
        isSatisfiable = dpll.dpllSatisfiable(clauses)
    else:
        plResolution = PLResolution()
        isSatisfiable = plResolution.plResolution(clauses)

    if not isSatisfiable:
        output_content = "no" + "\n"
        output_file = open("output.txt", 'w')
        output_file.write(output_content)
        sys.exit()
    # the sentence is satisfiable
    output_content = "yes" + "\n"
    p = 0.5
    walkSAT = WalkSAT()

    while True:
        model = walkSAT.walkSAT(clauses,p)
        if model is not None:
            break
        # else, redo it until the satisfiable model is found by trying another p value
        p = random.random()

    # print table assignment
    for person_index in range(1,num_person + 1):
        for table_index in range(1,num_table + 1):
            assign_value = model.assignments[propositionSymbolFactory.getPropositionSymbol("X[{},{}]".format(person_index,table_index))]
            if assign_value:
                output_content += "{} {}".format(person_index,table_index) + "\n"
                break

    output_file = open("output.txt", 'w')
    output_file.write(output_content)