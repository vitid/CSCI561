import sys
import copy
import itertools

class PropositionSymbol(object):
    def __init__(self,symbol):

        if len(symbol) == 0:
            raise Exception("PropositionSymbol should not be Empty")

        self.symbol = symbol

    def __eq__(self, other):
        if not isinstance(other,self.__class__):
            return False
        return self.symbol == other.symbol

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

    def getNumberLiterals(self):
        return len(self.literals)

    def isEmpty(self):
        return self.getNumberLiterals() == 0

    def getPositiveSymbols(self):
        return self._retrievePosOrNeg(True)

    def getNegativeSymbols(self):
        return self._retrievePosOrNeg(False)

    def isTautology(self):
        return len(self.getPositiveSymbols().intersection(self.getNegativeSymbols())) > 0

    def getClauseRepresentation(self):
        """
        :rtype: set[str]

        :return:
        """
        tokens = set()

        for l in self.literals: # type: Literal
            prefix = ""
            if l.isNegativeLiteral():
                prefix = "~"
            tokens.add(prefix + l.propositionSymbol.symbol)

        return tokens

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
        tokens = self.getClauseRepresentation()
        tokens = [t for t in tokens]
        tokens.sort()

        return hash(",".join(tokens))

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
        new_clauses = set()

        empty_clause = Clause([])

        while True:
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

        self.resolvePositiveWithNegative(ci,cj,resolvents)
        self.resolvePositiveWithNegative(cj,ci,resolvents)
        return resolvents

    def resolvePositiveWithNegative(self,c1,c2,resolvents):
        """
        @type c2: Clause
        @type c1: Clause

        :param c1:
        :param c2:
        :param resolvents:
        :return:
        """
        complementary = c1.getPositiveSymbols().intersection(c2.getNegativeSymbols())
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

if __name__ == "__main__":
    prop1 = PropositionSymbol("a")
    print prop1.symbol