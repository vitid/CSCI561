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
        self._hash = -1
        self._positiveSymbols = None
        self._negativeSymbols = None
        self._isTautology = None
        self._representation = None

    def getNumberLiterals(self):
        return len(self.literals)

    def isEmpty(self):
        return self.getNumberLiterals() == 0

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

        # cache what pair of clauses are already resolved to avoid unnecessary computation...
        resolve_clauses_cache = {}

        while True:

            # avoiding unnecessary .union(...) operation
            list_resolvents = list() # type: list[Clause]
            for pair in itertools.combinations(list(clauses),2):
                ci = pair[0] # type: Clause
                cj = pair[1] # type: Clause

                if (ci.getClauseRepresentation(),cj.getClauseRepresentation()) in resolve_clauses_cache or (cj.getClauseRepresentation(),ci.getClauseRepresentation()) in resolve_clauses_cache:
                    continue

                resolvents = self.plResolve(ci,cj)
                resolve_clauses_cache[(ci.getClauseRepresentation(),cj.getClauseRepresentation())] = 0
                resolve_clauses_cache[(cj.getClauseRepresentation(), ci.getClauseRepresentation())] = 0

                if empty_clause in resolvents:
                    return False

                list_resolvents += list(resolvents)
                #new_clauses = new_clauses.union(resolvents)

            #new_clauses = new_clauses.union(list_resolvents)
            new_clauses = list(new_clauses) + list_resolvents
            new_clauses = set(new_clauses)
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

if __name__ == "__main__":
    prop1 = PropositionSymbol("a")
    print prop1.symbol