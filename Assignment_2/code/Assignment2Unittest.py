from hw2cs561s2017 import *
import unittest

class TestKnowledgeRepresentation(unittest.TestCase):
    def setUp(self):
        self.propositionSymbolFactory = PropositionSymbolFactory()
        self.clauseHelper = ClauseHelper(self.propositionSymbolFactory)
        self.plResolution = PLResolution()
        self.dpll = DPLL()

        # initialize A,B,C,D,E symbols
        self.propositionSymbolFactory.getPropositionSymbol("A")
        self.propositionSymbolFactory.getPropositionSymbol("B")
        self.propositionSymbolFactory.getPropositionSymbol("C")
        self.propositionSymbolFactory.getPropositionSymbol("D")
        self.propositionSymbolFactory.getPropositionSymbol("E")

        # Book's example
        self.propositionSymbolFactory.getPropositionSymbol("P[2,1]")
        self.propositionSymbolFactory.getPropositionSymbol("B[1,1]")
        self.propositionSymbolFactory.getPropositionSymbol("P[1,2]")

    def test_Clause(self):
        self.assertEqual(self.clauseHelper.generateClause(["A", "B", "C"]).getNumberLiterals(), 3)
        self.assertEqual(self.clauseHelper.generateClause([]).getNumberLiterals(), 0)

        self.assertEqual(
            set([
                self.clauseHelper.generateClause(["A", "B", "C"]),
                self.clauseHelper.generateClause(["C", "B", "A"])
                ]
            ),
            set(
                [
                self.clauseHelper.generateClause(["B", "C", "A"])
                ]
            )
        )

        self.assertEqual("A,~B", self.clauseHelper.generateClause(["~B","A"]).getClauseRepresentation())
        self.assertEqual("~C", self.clauseHelper.generateClause(["~C"]).getClauseRepresentation())
        self.assertEqual("", self.clauseHelper.generateClause([]).getClauseRepresentation())

        self.assertTrue(self.clauseHelper.generateClause(["A","B","C","~B"]).isTautology())
        self.assertFalse(self.clauseHelper.generateClause(["C","~B"]).isTautology())
        # !!!
        self.assertFalse(self.clauseHelper.generateClause([]).isTautology())

    def test_PLResolutionPN0(self):
        resolvents = set()
        self.plResolution.resolveTwoClauses(self.clauseHelper.generateClause(["~A", "B", "C"]), self.clauseHelper.generateClause(["~A", "B", "C"]), resolvents)
        self.assertEqual(resolvents,set())

    def test_PLResolutionPN1(self):
        resolvents = set()
        self.plResolution.resolveTwoClauses(self.clauseHelper.generateClause(["A", "B"]), self.clauseHelper.generateClause(["B", "~A"]), resolvents)
        self.assertEqual(resolvents, set( [self.clauseHelper.generateClause(["B"])] ))
        self.assertNotEqual(resolvents, set([self.clauseHelper.generateClause(["~B"])]))

    def test_PLResolutionPN2(self):
        resolvents = set()
        self.plResolution.resolveTwoClauses(self.clauseHelper.generateClause(["A", "B"]), self.clauseHelper.generateClause(["B", "~A", "C"]), resolvents)
        self.assertEqual(resolvents, set( [self.clauseHelper.generateClause(["C","B"])] ))

    def test_PLResolutionPN3(self):
        resolvents = set()
        self.plResolution.resolveTwoClauses(self.clauseHelper.generateClause(["A", "B", "~D"]), self.clauseHelper.generateClause(["D", "B", "~A", "C"]), resolvents)
        # get Tautology
        self.assertEqual(resolvents, set())

    def test_PLResolutionPN4(self):
        resolvents = set()
        self.plResolution.resolveTwoClauses(self.clauseHelper.generateClause(["A", "B", "~D"]), self.clauseHelper.generateClause(["B", "~A", "C", "~E"]), resolvents)
        # get Tautology
        self.assertEqual(resolvents, set([self.clauseHelper.generateClause(["B","~D","C","~E"])]))

    def test_PLResolutionPN5(self):
        resolvents = set()
        self.plResolution.resolveTwoClauses(self.clauseHelper.generateClause(["A", "B", "~D", "E"]), self.clauseHelper.generateClause(["B", "~A", "C", "~E"]), resolvents)
        # get Tautology
        self.assertEqual(resolvents, set())

    def test_PLResolve0(self):
        resolvents = self.plResolution.plResolve(self.clauseHelper.generateClause(["A", "B","~D","E"]),self.clauseHelper.generateClause(["B","~A","C","~E"]))
        self.assertEqual(resolvents, set())

    def test_PLResolve1(self):
        resolvents = self.plResolution.plResolve(self.clauseHelper.generateClause(["B","~A","C","~E"]),self.clauseHelper.generateClause(["A", "B","~D","E"]))
        self.assertEqual(resolvents, set())

    def test_PLResolve2(self):
        resolvents = self.plResolution.plResolve(self.clauseHelper.generateClause(["B","A","C","~E"]),self.clauseHelper.generateClause(["~A", "B","~D","E"]))
        self.assertEqual(resolvents, set())

    def test_PLResolve3(self):
        resolvents = self.plResolution.plResolve(self.clauseHelper.generateClause(["B","A","C","~E"]),self.clauseHelper.generateClause(["B","~D","E"]))
        self.assertEqual(resolvents, set([self.clauseHelper.generateClause(["B","A","C","~D"])]))

    def test_PLResolve4(self):
        resolvents = self.plResolution.plResolve(self.clauseHelper.generateClause(["B","A","C","~E"]),self.clauseHelper.generateClause([]))
        self.assertEqual(resolvents, set())

    def test_PLResolve5(self):
        resolvents = self.plResolution.plResolve(self.clauseHelper.generateClause(["A"]),
                                                 self.clauseHelper.generateClause(["~A"]) )
        self.assertEqual(resolvents, set( [ self.clauseHelper.generateClause([]) ] ))

    def test_PLResolve6(self):
        resolvents = self.plResolution.plResolve(self.clauseHelper.generateClause(["~A"]),
                                                 self.clauseHelper.generateClause(["A"]) )
        self.assertEqual(resolvents, set( [ self.clauseHelper.generateClause([]) ] ))

    def test_PLResolve_Book_Example0(self):
        resolvents = self.plResolution.plResolve(self.clauseHelper.generateClause(["~P[2,1]","B[1,1]"]),
                                                 self.clauseHelper.generateClause(["~B[1,1]","P[1,2]","P[2,1]"]) )
        self.assertEqual(resolvents, set([]))

    def test_PLResolve_Book_Example1(self):
        resolvents = self.plResolution.plResolve(self.clauseHelper.generateClause(["~P[2,1]","B[1,1]"]),
                                                 self.clauseHelper.generateClause(["~B[1,1]"]) )
        self.assertEqual(resolvents, set([self.clauseHelper.generateClause(["~P[2,1]"])]))

    def test_PLResolve_Book_Example2(self):
        resolvents = self.plResolution.plResolve(self.clauseHelper.generateClause(["~B[1,1]","P[1,2]","P[2,1]"]),                                                 self.clauseHelper.generateClause(["~P[1,2]","B[1,1]"]) )
        self.assertEqual(resolvents, set([]))

    def test_PLResolve_Book_Example3(self):
        resolvents = self.plResolution.plResolve(self.clauseHelper.generateClause(["~P[1,2]","B[1,1]"]),                                                          self.clauseHelper.generateClause(["~B[1,1]"]) )
        self.assertEqual(resolvents, set([self.clauseHelper.generateClause(["~P[1,2]"])]))

    def test_PLResolve_Book_Example4(self):
        resolvents = self.plResolution.plResolve(self.clauseHelper.generateClause(["~P[1,2]"]),                                                 self.clauseHelper.generateClause(["P[1,2]"]) )
        self.assertEqual(resolvents, set([self.clauseHelper.generateClause([])]))

    def test_PLResolution0(self):
        clauses = set() # type:set[clauses]
        clauses.add(self.clauseHelper.generateClause(["A"]))

        self.assertTrue(self.plResolution.plResolution(clauses))

    def test_PLResolution1(self):
        clauses = set() # type:set[clauses]
        clauses.add(self.clauseHelper.generateClause(["~A"]))

        self.assertTrue(self.plResolution.plResolution(clauses))

    def test_PLResolution2(self):
        clauses = set() # type:set[clauses]
        clauses.add(self.clauseHelper.generateClause(["A","B"]))
        clauses.add(self.clauseHelper.generateClause(["A", "~B"]))

        self.assertTrue(self.plResolution.plResolution(clauses))

    def test_PLResolution_Book0(self):
        clauses = set() # type:set[clauses]
        clauses.add(self.clauseHelper.generateClause(["~P[1,2]","B[1,1]"]))
        clauses.add(self.clauseHelper.generateClause(["~B[1,1]", "P[1,2]","P[2,1]"]))
        clauses.add(self.clauseHelper.generateClause(["~P[1,2]", "B[1,1]"]))
        clauses.add(self.clauseHelper.generateClause(["~B[1,1]"]))
        clauses.add(self.clauseHelper.generateClause(["P[1,2]"]))

        self.assertFalse(self.plResolution.plResolution(clauses))

    def test_comparatorFunctions(self):

        self.assertTrue(self.clauseHelper.getLiteral("A").isPositiveLiteral())
        self.assertTrue(self.clauseHelper.getLiteral("B").isPositiveLiteral())
        self.assertTrue(self.clauseHelper.getLiteral("C").isPositiveLiteral())
        self.assertFalse(self.clauseHelper.getLiteral("~C").isPositiveLiteral())
        self.assertTrue(self.clauseHelper.getLiteral("~C").isNegativeLiteral())

        self.assertTrue(self.clauseHelper.getLiteral("A") == self.clauseHelper.getLiteral("A"))
        self.assertTrue(self.clauseHelper.getLiteral("~C") == self.clauseHelper.getLiteral("~C"))
        self.assertFalse(self.clauseHelper.getLiteral("C") == self.clauseHelper.getLiteral("~C"))

        self.assertTrue(self.clauseHelper.generateClause(["~A","B","C"]) == self.clauseHelper.generateClause(["C","B","~A"]))
        self.assertFalse(self.clauseHelper.generateClause(["~A", "B", "C"]) == self.clauseHelper.generateClause(["C", "B", "A"]))

        # !!Empty clause is not tautology !!
        self.assertFalse(self.clauseHelper.generateClause([]).isTautology())

    def test_getClausesOnePersonAtOneTable0(self):
        ko = KnowledgeOperator(3,2,[],[],self.clauseHelper)
        expected = {
            self.clauseHelper.generateClause(["X[1,1]","X[1,2]"]),
            self.clauseHelper.generateClause(["X[2,1]", "X[2,2]"]),
            self.clauseHelper.generateClause(["X[3,1]", "X[3,2]"]),
            self.clauseHelper.generateClause(["~X[1,1]", "~X[1,2]"]),
            self.clauseHelper.generateClause(["~X[2,1]", "~X[2,2]"]),
            self.clauseHelper.generateClause(["~X[3,1]", "~X[3,2]"]),
        }
        self.assertEqual(ko.getClausesOnePersonAtOneTable(),expected)

    def test_getClausesOnePersonAtOneTable1(self):
        ko = KnowledgeOperator(2,3,[],[],self.clauseHelper)
        expected = {
            self.clauseHelper.generateClause(["X[1,1]","X[1,2]","X[1,3]"]),
            self.clauseHelper.generateClause(["X[2,1]", "X[2,2]","X[2,3]"]),

            self.clauseHelper.generateClause(["~X[1,1]", "~X[1,2]"]),
            self.clauseHelper.generateClause(["~X[1,1]", "~X[1,3]"]),
            self.clauseHelper.generateClause(["~X[1,2]", "~X[1,3]"]),

            self.clauseHelper.generateClause(["~X[2,1]", "~X[2,2]"]),
            self.clauseHelper.generateClause(["~X[2,1]", "~X[2,3]"]),
            self.clauseHelper.generateClause(["~X[2,2]", "~X[2,3]"]),
        }
        self.assertEqual(ko.getClausesOnePersonAtOneTable(),expected)

    def test_getClausesFriend0(self):
        ko = KnowledgeOperator(3, 2, [(1, 2), (2, 3)], [], self.clauseHelper)
        expected = {
            self.clauseHelper.generateClause(["~X[1,1]", "X[2,1]"]),
            self.clauseHelper.generateClause(["X[1,1]", "~X[2,1]"]),
            self.clauseHelper.generateClause(["~X[1,2]", "X[2,2]"]),
            self.clauseHelper.generateClause(["X[1,2]", "~X[2,2]"]),

            self.clauseHelper.generateClause(["~X[2,1]", "X[3,1]"]),
            self.clauseHelper.generateClause(["X[2,1]", "~X[3,1]"]),
            self.clauseHelper.generateClause(["~X[2,2]", "X[3,2]"]),
            self.clauseHelper.generateClause(["X[2,2]", "~X[3,2]"])
        }
        self.assertEqual(ko.getClausesFriend(), expected)

    def test_getClausesEnemy0(self):
        ko = KnowledgeOperator(3,2,[],[(1,2),(2,3)],self.clauseHelper)
        expected = {
            self.clauseHelper.generateClause(["~X[1,1]","~X[2,1]"]),
            self.clauseHelper.generateClause(["~X[1,2]", "~X[2,2]"]),
            self.clauseHelper.generateClause(["~X[2,1]", "~X[3,1]"]),
            self.clauseHelper.generateClause(["~X[2,2]", "~X[3,2]"]),
        }
        self.assertEqual(ko.getClausesEnemy(),expected)

    def test_TATestCase1(self):
        """
        Input:
        4 1
        1 2 F
        2 3 F
        3 4 F

        Output: yes
        :return:
        """
        ko = KnowledgeOperator(4, 1, [(1,2),(2,3),(3,4)], [], self.clauseHelper)
        self.assertTrue(self.plResolution.plResolution(ko.getAssociatedClauses()))
        self.assertTrue(self.dpll.dpllSatisfiable(ko.getAssociatedClauses()))

    def test_TATestCase2(self):
        """
        Input:
        5 1
        1 3 E
        1 2 F
        4 5 F

        Output: no
        :return:
        """
        ko = KnowledgeOperator(5, 1, [(1,2),(4,5)], [(1,3)], self.clauseHelper)
        self.assertFalse(self.plResolution.plResolution(ko.getAssociatedClauses()))
        self.assertFalse(self.dpll.dpllSatisfiable(ko.getAssociatedClauses()))

    def test_TATestCase3(self):
        """
        Input:
        8 10
        1 2 E
        2 5 E
        6 7 E
        7 8 E

        Output: yes
        :return:
        """
        ko = KnowledgeOperator(8, 10, [], [(1,2),(2,5),(6,7),(7,8)], self.clauseHelper)
        # PL Resolution is exploded
        #self.assertTrue(self.plResolution.plResolution(ko.getAssociatedClauses()))
        self.assertTrue(self.dpll.dpllSatisfiable(ko.getAssociatedClauses()))

    def test_TATestCase4(self):
        """
        Input:
        6 2
        1 2 F
        2 4 F
        4 6 F
        1 6 E

        Output: no
        :return:
        """
        ko = KnowledgeOperator(6, 2, [(1,2),(2,4),(4,6)], [(1,6)], self.clauseHelper)
        self.assertFalse(self.plResolution.plResolution(ko.getAssociatedClauses()))
        self.assertFalse(self.dpll.dpllSatisfiable(ko.getAssociatedClauses()))

    def test_TATestCase5(self):
        """
        Input:
        9 3
        1 2 E
        1 3 F
        1 8 F
        2 4 F
        3 7 E
        5 6 F
        6 9 F
        8 9 E

        Output: yes
        :return:
        """
        ko = KnowledgeOperator(9, 3, [(1,3),(1,8),(2,4),(5,6),(6,9)], [(1,2),(3,7),(8,9)], self.clauseHelper)
        # PL Resolution is exploded
        #self.assertTrue(self.plResolution.plResolution(ko.getAssociatedClauses()))
        self.assertTrue(self.dpll.dpllSatisfiable(ko.getAssociatedClauses()))

    def test_CustomTestCase0(self):
        """
        Input:
        13 14
        5 1 E
        2 3 F

        Output: yes
        :return:
        """
        ko = KnowledgeOperator(13, 14, [(2,3)], [(5,1)], self.clauseHelper)
        self.assertTrue(self.dpll.dpllSatisfiable(ko.getAssociatedClauses()))

    def test_CustomTestCase1(self):
        """
        Input:
        2 1
        1 2 E

        Output: no
        :return:
        """
        ko = KnowledgeOperator(2, 1, [], [(1,2)], self.clauseHelper)
        self.assertFalse(self.dpll.dpllSatisfiable(ko.getAssociatedClauses()))

    def test_CustomTestCase2(self):
        """
        Input:
        15 3
        1 2 E
        3 4 E
        5 6 E
        7 8 E
        9 10 E
        11 12 E
        7 9 E

        Output: yes
        :return:
        """
        ko = KnowledgeOperator(15, 3, [], [(1,2),(3,4),(5,6),(7,8),(9,10),(11,12),(7,9)], self.clauseHelper)
        self.assertTrue(self.dpll.dpllSatisfiable(ko.getAssociatedClauses()))

    def test_CustomTestCase3(self):
        """
        Input:
        15 3
        1 2 E
        3 4 E
        5 6 E
        7 8 E
        9 10 E
        11 12 E
        7 9 E
        4 3 F

        Output: no
        :return:
        """
        ko = KnowledgeOperator(15, 3, [(4,3)], [(1,2),(3,4),(5,6),(7,8),(9,10),(11,12),(7,9)], self.clauseHelper)
        self.assertFalse(self.dpll.dpllSatisfiable(ko.getAssociatedClauses()))

    def test_CustomTestCase4(self):
        """
        Input:
        30 3
        1 2 E
        3 4 E
        5 6 E
        7 8 E
        9 10 E
        11 12 E
        12 13 E
        13 14 E
        14 15 E
        15 16 E
        17 16 E
        17 18 E
        19 18 E
        19 20 E
        21 20 E
        21 22 E
        23 22 E
        23 24 E
        25 24 E
        25 26 E
        27 26 E
        27 28 E
        29 28 E
        29 30 E
        30 1 F
        1 5 F
        5 9 F
        9 13 F
        13 17 F
        17 21 F
        21 25 F

        Output: yes
        :return:
        """
        ko = KnowledgeOperator(30, 3, [(1,30),(1,5),(5,9),(9,13),(13,17),(17,21),(21,25)], [(1,2),(3,4),(5,6),(7,8),(9,10),(11,12),(12,13),(13,14),(14,15),(15,16),(16,17),(17,18),(18,19),(19,20),(20,21),(21,22),(22,23),(23,24),(24,25),(25,26),(26,27),(27,28),(28,29),(29,30)], self.clauseHelper)
        self.assertTrue(self.dpll.dpllSatisfiable(ko.getAssociatedClauses()))

    def test_determineValue0(self):
        model = Model({PropositionSymbol("A"):True})
        self.assertTrue(model.determineValue(self.clauseHelper.generateClause(["A"])))
        self.assertFalse(model.determineValue(self.clauseHelper.generateClause(["~A"])))

    def test_determineValue1(self):
        model = Model({PropositionSymbol("A"):True,PropositionSymbol("B"):True,PropositionSymbol("C"):False})
        self.assertTrue(model.determineValue(self.clauseHelper.generateClause(["A","B","C"])))
        self.assertTrue(model.determineValue(self.clauseHelper.generateClause(["~A", "B", "C"])))
        self.assertTrue(model.determineValue(self.clauseHelper.generateClause(["~A", "~B", "~C"])))
        self.assertFalse(model.determineValue(self.clauseHelper.generateClause(["~A", "~B", "C"])))

        self.assertTrue(model.determineValue(self.clauseHelper.generateClause(["D","~D"])))

    def test_satisfies0(self):
        model = Model({PropositionSymbol("A"): True, PropositionSymbol("B"): True, PropositionSymbol("C"): False})
        self.assertTrue(model.satisfies(set([
            self.clauseHelper.generateClause(["A"]),
            self.clauseHelper.generateClause(["B"]),
            self.clauseHelper.generateClause(["~C"])
            ])))

        self.assertFalse(model.satisfies(set([
            self.clauseHelper.generateClause(["A"]),
            self.clauseHelper.generateClause(["B"]),
            self.clauseHelper.generateClause(["C"])
        ])))

        self.assertTrue(model.satisfies(set([
            self.clauseHelper.generateClause(["A","B","C"])
        ])))

        self.assertTrue(model.satisfies(set([
            self.clauseHelper.generateClause(["A", "B"]),
            self.clauseHelper.generateClause(["~A", "~C"]),
        ])))

        self.assertFalse(model.satisfies(set([
            self.clauseHelper.generateClause(["A", "B"]),
            self.clauseHelper.generateClause(["~A", "C"]),
        ])))

    def test_flip0(self):
        model = Model({PropositionSymbol("A"): True, PropositionSymbol("B"): True, PropositionSymbol("C"): False})
        self.assertEqual(model.flip(PropositionSymbol("A")).assignments, {PropositionSymbol("A"): False, PropositionSymbol("B"): True, PropositionSymbol("C"): False})
        self.assertEqual(model.flip(PropositionSymbol("C")).assignments,
                         {PropositionSymbol("A"): True, PropositionSymbol("B"): True, PropositionSymbol("C"): True})
        # sign of the original model is not changed
        self.assertEqual(model.assignments,
                         {PropositionSymbol("A"): True, PropositionSymbol("B"): True, PropositionSymbol("C"): False})

    def test_randomAssignmentToSymbolsInClauses0(self):
        walkSAT = WalkSAT()
        assignments = walkSAT.randomAssignmentToSymbolsInClauses(
            set([
                self.clauseHelper.generateClause(["A", "B"]),
                self.clauseHelper.generateClause(["~A", "C"]),
                self.clauseHelper.generateClause(["~D"])
            ])
        ).assignments
        assigned_symbol = set([s.symbol for s in assignments])
        self.assertEqual(assigned_symbol,set(["A","B","C","D"]))

    def test_walkSAT0(self):
        walkSAT = WalkSAT()
        clauses = set([
                self.clauseHelper.generateClause(["A", "B"]),
                self.clauseHelper.generateClause(["~A", "C"]),
                self.clauseHelper.generateClause(["~D"])
            ])
        model = walkSAT.walkSAT(clauses,0.5,100)
        self.assertTrue(model.satisfies(clauses))

    def test_walkSAT1(self):
        walkSAT = WalkSAT()
        clauses = set([
                self.clauseHelper.generateClause(["A"]),
                self.clauseHelper.generateClause(["~A"])
            ])
        model = walkSAT.walkSAT(clauses,0.5,100)
        self.assertIsNone(model)

    def test_TATestCase1_walkSAT(self):
        """
        Input:
        4 1
        1 2 F
        2 3 F
        3 4 F

        Output: yes
        :return:
        """
        ko = KnowledgeOperator(4, 1, [(1,2),(2,3),(3,4)], [], self.clauseHelper)
        walkSAT = WalkSAT(100)
        model = walkSAT.walkSAT(ko.getAssociatedClauses(), 0.5, 100)
        self.assertTrue(model.satisfies(ko.getAssociatedClauses()))

    def test_TATestCase2_walkSAT(self):
        """
        Input:
        5 1
        1 3 E
        1 2 F
        4 5 F

        Output: no
        :return:
        """
        ko = KnowledgeOperator(5, 1, [(1,2),(4,5)], [(1,3)], self.clauseHelper)
        walkSAT = WalkSAT(100)
        model = walkSAT.walkSAT(ko.getAssociatedClauses(), 0.5, 100)
        self.assertIsNone(model)

    def test_TATestCase3_walkSAT(self):
        """
        Input:
        8 10
        1 2 E
        2 5 E
        6 7 E
        7 8 E

        Output: yes
        :return:
        """
        ko = KnowledgeOperator(8, 10, [], [(1,2),(2,5),(6,7),(7,8)], self.clauseHelper)
        walkSAT = WalkSAT(100)
        model = walkSAT.walkSAT(ko.getAssociatedClauses(), 0.5, 100)
        self.assertTrue(model.satisfies(ko.getAssociatedClauses()))

    def test_TATestCase4_walkSAT(self):
        """
        Input:
        6 2
        1 2 F
        2 4 F
        4 6 F
        1 6 E

        Output: no
        :return:
        """
        ko = KnowledgeOperator(6, 2, [(1, 2), (2, 4), (4, 6)], [(1, 6)], self.clauseHelper)
        walkSAT = WalkSAT(100)
        model = walkSAT.walkSAT(ko.getAssociatedClauses(), 0.5, 100)
        self.assertIsNone(model)

    def test_TATestCase5_walkSAT(self):
        """
        Input:
        9 3
        1 2 E
        1 3 F
        1 8 F
        2 4 F
        3 7 E
        5 6 F
        6 9 F
        8 9 E

        Output: yes
        :return:
        """
        ko = KnowledgeOperator(9, 3, [(1, 3), (1, 8), (2, 4), (5, 6), (6, 9)], [(1, 2), (3, 7), (8, 9)],self.clauseHelper)
        walkSAT = WalkSAT(100)
        model = walkSAT.walkSAT(ko.getAssociatedClauses(), 0.5, 100)
        self.assertTrue(model.satisfies(ko.getAssociatedClauses()))

    def test_CustomTestCase0_walkSAT(self):
        """
        Input:
        13 14
        5 1 E
        2 3 F

        Output: yes
        :return:
        """
        ko = KnowledgeOperator(13, 14, [(2,3)], [(5,1)], self.clauseHelper)
        walkSAT = WalkSAT(100)
        model = walkSAT.walkSAT(ko.getAssociatedClauses(), 0.5, 100)
        self.assertTrue(model.satisfies(ko.getAssociatedClauses()))

    def test_CustomTestCase3_walkSAT(self):
        """
        Input:
        15 3
        1 2 E
        3 4 E
        5 6 E
        7 8 E
        9 10 E
        11 12 E
        7 9 E

        Output: yes
        :return:
        """
        ko = KnowledgeOperator(15, 3, [], [(1,2),(3,4),(5,6),(7,8),(9,10),(11,12),(7,9)], self.clauseHelper)
        walkSAT = WalkSAT(100)
        model = walkSAT.walkSAT(ko.getAssociatedClauses(), 0.5, 100)
        self.assertTrue(model.satisfies(ko.getAssociatedClauses()))

    def test_CustomTestCase4_walkSAT(self):
        """
        Input:
        30 3
        1 2 E
        3 4 E
        5 6 E
        7 8 E
        9 10 E
        11 12 E
        12 13 E
        13 14 E
        14 15 E
        15 16 E
        17 16 E
        17 18 E
        19 18 E
        19 20 E
        21 20 E
        21 22 E
        23 22 E
        23 24 E
        25 24 E
        25 26 E
        27 26 E
        27 28 E
        29 28 E
        29 30 E
        30 1 F
        1 5 F
        5 9 F
        9 13 F
        13 17 F
        17 21 F
        21 25 F

        Output: yes
        :return:
        """
        ko = KnowledgeOperator(30, 3, [(1,30),(1,5),(5,9),(9,13),(13,17),(17,21),(21,25)], [(1,2),(3,4),(5,6),(7,8),(9,10),(11,12),(12,13),(13,14),(14,15),(15,16),(16,17),(17,18),(18,19),(19,20),(20,21),(21,22),(22,23),(23,24),(24,25),(25,26),(26,27),(27,28),(28,29),(29,30)], self.clauseHelper)
        walkSAT = WalkSAT(100)
        model = walkSAT.walkSAT(ko.getAssociatedClauses(), 0.5, 1000)
        self.assertTrue(model.satisfies(ko.getAssociatedClauses()))

if __name__ == '__main__':
    unittest.main()