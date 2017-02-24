from hw2cs561s2017 import *
import unittest

class TestKnowledgeRepresentation(unittest.TestCase):
    def setUp(self):
        self.propositionSymbolFactory = PropositionSymbolFactory()
        self.clauseHelper = ClauseHelper(self.propositionSymbolFactory)
        self.plResolution = PLResolution()

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

        self.assertEqual(set(["A","~B"]), self.clauseHelper.generateClause(["~B","A"]).getClauseRepresentation())
        self.assertEqual(set(["~C"]), self.clauseHelper.generateClause(["~C"]).getClauseRepresentation())
        self.assertEqual(set([]), self.clauseHelper.generateClause([]).getClauseRepresentation())

        self.assertTrue(self.clauseHelper.generateClause(["A","B","C","~B"]).isTautology())
        self.assertFalse(self.clauseHelper.generateClause(["C","~B"]).isTautology())
        # !!!
        self.assertFalse(self.clauseHelper.generateClause([]).isTautology())

    def test_PLResolutionPN0(self):
        resolvents = set()
        self.plResolution.resolvePositiveWithNegative(self.clauseHelper.generateClause(["~A", "B", "C"]),self.clauseHelper.generateClause(["~A", "B", "C"]),resolvents)
        self.assertEqual(resolvents,set())

    def test_PLResolutionPN1(self):
        resolvents = set()
        self.plResolution.resolvePositiveWithNegative(self.clauseHelper.generateClause(["A", "B"]),self.clauseHelper.generateClause(["B","~A"]),resolvents)
        self.assertEqual(resolvents, set( [self.clauseHelper.generateClause(["B"])] ))
        self.assertNotEqual(resolvents, set([self.clauseHelper.generateClause(["~B"])]))

    def test_PLResolutionPN2(self):
        resolvents = set()
        self.plResolution.resolvePositiveWithNegative(self.clauseHelper.generateClause(["A", "B"]),self.clauseHelper.generateClause(["B","~A","C"]),resolvents)
        self.assertEqual(resolvents, set( [self.clauseHelper.generateClause(["C","B"])] ))

    def test_PLResolutionPN3(self):
        resolvents = set()
        self.plResolution.resolvePositiveWithNegative(self.clauseHelper.generateClause(["A", "B","~D"]),self.clauseHelper.generateClause(["D","B","~A","C"]),resolvents)
        # get Tautology
        self.assertEqual(resolvents, set())

    def test_PLResolutionPN4(self):
        resolvents = set()
        self.plResolution.resolvePositiveWithNegative(self.clauseHelper.generateClause(["A", "B","~D"]),self.clauseHelper.generateClause(["B","~A","C","~E"]),resolvents)
        # get Tautology
        self.assertEqual(resolvents, set([self.clauseHelper.generateClause(["B","~D","C","~E"])]))

    def test_PLResolutionPN5(self):
        resolvents = set()
        self.plResolution.resolvePositiveWithNegative(self.clauseHelper.generateClause(["A", "B","~D","E"]),self.clauseHelper.generateClause(["B","~A","C","~E"]),resolvents)
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

if __name__ == '__main__':
    unittest.main()