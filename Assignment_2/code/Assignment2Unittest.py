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

    def test_PLResolution0(self):
        resolvents = set()
        self.plResolution.resolvePositiveWithNegative(self.clauseHelper.generateClause(["~A", "B", "C"]),self.clauseHelper.generateClause(["~A", "B", "C"]),resolvents)
        self.assertEqual(resolvents,set())

    def test_PLResolution1(self):
        resolvents = set()
        self.plResolution.resolvePositiveWithNegative(self.clauseHelper.generateClause(["A", "B"]),self.clauseHelper.generateClause(["B","~A"]),resolvents)
        self.assertEqual(resolvents, set( [self.clauseHelper.generateClause(["B"])] ))
        self.assertNotEqual(resolvents, set([self.clauseHelper.generateClause(["~B"])]))

    def test_PLResolution2(self):
        resolvents = set()
        self.plResolution.resolvePositiveWithNegative(self.clauseHelper.generateClause(["A", "B"]),self.clauseHelper.generateClause(["B","~A","C"]),resolvents)
        self.assertEqual(resolvents, set( [self.clauseHelper.generateClause(["C","B"])] ))

    def test_PLResolution3(self):
        resolvents = set()
        self.plResolution.resolvePositiveWithNegative(self.clauseHelper.generateClause(["A", "B","~D"]),self.clauseHelper.generateClause(["D","B","~A","C"]),resolvents)
        # get Tautology
        self.assertEqual(resolvents, set())

    def test_PLResolution4(self):
        resolvents = set()
        self.plResolution.resolvePositiveWithNegative(self.clauseHelper.generateClause(["A", "B","~D"]),self.clauseHelper.generateClause(["B","~A","C","~E"]),resolvents)
        # get Tautology
        self.assertEqual(resolvents, set([self.clauseHelper.generateClause(["B","~D","C","~E"])]))

    def test_PLResolution5(self):
        resolvents = set()
        self.plResolution.resolvePositiveWithNegative(self.clauseHelper.generateClause(["A", "B","~D","E"]),self.clauseHelper.generateClause(["B","~A","C","~E"]),resolvents)
        # get Tautology
        self.assertEqual(resolvents, set())

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

if __name__ == '__main__':
    unittest.main()