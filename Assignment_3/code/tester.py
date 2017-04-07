import unittest

from hw3cs561s2017 import *

class TestSuite(unittest.TestCase):
    def setUp(self):
        self.createBn0()
        self.createBn1()

    def createBn0(self):
        node_L = Node("L", prob=0.4)
        node_N = Node("N", parents=[node_L], condprob={
            (True,): 0.8,
            (False,): 0.3
        })
        node_I = Node("I", prob=0.5)
        node_D = Node("D", parents=[node_N, node_I], condprob={
            (True, True): 0.3,
            (True, False): 0.6,
            (False, True): 0.95,
            (False, False): 0.05,
        })
        self.bn0 = BayesNet([node_L, node_N, node_I, node_D])

    def createBn1(self):
        node_L = Node("L", prob=0.4)
        node_N = Node("N", parents=[node_L], condprob={
            (True,): 0.8,
            (False,): 0.3
        })
        node_I = Node("I", prob=1.0, is_decision_node=True)
        node_D = Node("D", parents=[node_N, node_I], condprob={
            (True, True): 0.3,
            (True, False): 0.6,
            (False, True): 0.95,
            (False, False): 0.05,
        })
        node_Utility = UtilityNode("Utility", parents=[node_D], condUtility={
            (True,): 100,
            (False,): -10
        })
        self.bn1 = BayesNet([node_L, node_N, node_I, node_D],utility_node=node_Utility)

    def createBnTest7(self):
        node_A = Node("A",prob=0.3)
        node_B = Node("B",prob=0.6)
        node_C = Node("C",prob=0.4)
        node_D = Node("D",prob=0.2)
        node_I = Node("I",prob=0.6)
        node_E = Node("D", parents=[node_A,node_B,node_C,node_D], condprob={
            (True, True, True, True): 0.5,
            (True, True, True, False): 0,
            (True, True, False, True): 0,
            (True, True, True, True): 0,
            (True, True, True, True): 0,
            (True, True, True, True): 0,
            (True, True, True, True): 0,
            (True, True, True, True): 0,
            (True, True, True, True): 0,
            (True, True, True, True): 0,
            (True, True, True, True): 0,
            (True, True, True, True): 0,
            (True, True, True, True): 0,
            (True, True, True, True): 0,
            (True, True, True, True): 0,
            (True, True, True, True): 0,
        })

    def test_queryGiven(self):
        test_cases = [
            ("L",{"L":True},0.4),
            ("L", {"L": False}, 0.6),
            ("N", {"L": True,"N": True}, 0.8),
            ("N", {"L": True, "N": False}, 0.2),
            ("D", {"D":True,"L":True,"I":True,"N":False}, 0.95),
            ("D", {"D": False, "L": True, "I": True, "N": False}, 0.05)
        ]
        for test_case in test_cases:
            self.assertEqual(round(self.bn1.queryGiven(test_case[0],test_case[1]),2),test_case[2])

    def test_sortTopology(self):
        self.assertEqual(self.bn1.sortTopology(),["I","L","N","D"])

    def test_queryProb(self):
        test_cases = [
            ({"N": True}, {"N":True,"D":True}, 1.00),
            ({"N": False}, {"N": True, "D": True}, 0.00),
            ({"N":True,"I":False},{},0.25),
            ({"D":True}, {"L":True,"I":True}, 0.43),
        ]
        for test_case in test_cases:
            self.assertEqual(round(self.bn0.queryProb(test_case[0], test_case[1]), 2), test_case[2])

        test_cases = [
            ({"D": True}, {"L":False,"I":True}, 0.76),
        ]
        for test_case in test_cases:
            self.assertEqual(round(self.bn1.queryProb(test_case[0], test_case[1]), 2), test_case[2])

    def test_getExpectedUtility(self):
        test_cases = [
            ({"I": True}, 59),
            ({"I": True,"L":True}, 37),
        ]
        for test_case in test_cases:
            self.assertEqual(int(round(self.bn1.getExpectedUtility(test_case[0]))),test_case[1])

    def test_getMaximumExpectedUtility(self):
        test_cases = [
            (["I"],{}, ((True,),59)),
            (["I"], {"L":True}, ((False,),44)),
        ]
        for test_case in test_cases:
            r = self.bn1.getMaximumExpectedUtility(test_case[0],test_case[1])
            r = (r[0],int(round(r[1])))
            self.assertEqual(r,test_case[2])

    def test_constructPQuery(self):
        line = "P(D = + | L = -, I = +)"
        query = Query.constructQuery(line) #type: Query
        self.assertEqual(query.query_type,Query.P_Query)
        self.assertEqual(len(query.ask_variables), 1)
        self.assertEqual(len(query.evidents), 2)
        self.assertEqual(query.ask_variables,{"D":True})
        self.assertEqual(query.evidents, {"L":False,"I": True})

    def test_constructEUQuery0(self):
        line = "EU(I = +)"
        query = Query.constructQuery(line) #type: Query
        self.assertEqual(query.query_type,Query.EU_Query)
        self.assertEqual(len(query.evidents), 1)
        self.assertEqual(query.evidents, {"I": True})

    def test_constructEUQuery1(self):
        line = "EU(I = + | L = +)"
        query = Query.constructQuery(line) #type: Query
        self.assertEqual(query.query_type,Query.EU_Query)
        self.assertEqual(len(query.evidents), 2)
        self.assertEqual(query.evidents, {"I": True, "L": True})

    def test_constructMEUQuery0(self):
        line = "MEU(I)"
        query = Query.constructQuery(line) #type: Query
        self.assertEqual(query.query_type,Query.MEU_Query)
        self.assertEqual(len(query.evidents), 0)
        self.assertEqual(query.decision_nodes, ["I"])

    def test_constructMEUQuery1(self):
        line = "MEU(I | L = +)"
        query = Query.constructQuery(line) #type: Query
        self.assertEqual(query.query_type,Query.MEU_Query)
        self.assertEqual(len(query.evidents), 1)
        self.assertEqual(query.evidents, {"L":True})
        self.assertEqual(query.decision_nodes, ["I"])

    def test_constructDecisionNode(self):
        lines = [
                 "I",
                 "decision"
                ]
        node = Node.constructNode(lines,{})
        self.assertEqual(node.isDecisionNode(),True)
        self.assertEqual(node.node_name,"I")

    def test_constructRootNode(self):
        lines = [
                 "L",
                 "0.4"
                ]
        node = Node.constructNode(lines,{})
        self.assertEqual(node.isDecisionNode(), False)
        self.assertEqual(node.node_name, "L")
        self.assertEqual(node.prob, 0.4)

    def test_constructNode(self):
        node_L = Node("L", prob=0.4)
        nodes_dict = {}
        nodes_dict["L"] = node_L
        lines = [
            "N | L",
            "0.8 +",
            "0.3 -"
        ]
        node_N = Node.constructNode(lines,nodes_dict)
        self.assertEqual(node_N.isDecisionNode(), False)
        self.assertEqual(node_N.node_name, "N")
        self.assertEqual(node_N.parents,[node_L])
        self.assertEqual(node_N.prob, -1)
        self.assertEqual(node_N.condprob,{(True,):0.8,(False,):0.3})

        nodes_dict["N"] = node_N

        node_I = Node("I", prob=1.0, is_decision_node=True)

        nodes_dict["I"] = node_I

        lines = [
            "D | N I",
            "0.3 + +",
            "0.6 + -",
            "0.95 - +",
            "0.05 - -"
        ]
        node_D = Node.constructNode(lines, nodes_dict)
        self.assertEqual(node_D.isDecisionNode(), False)
        self.assertEqual(node_D.node_name, "D")
        self.assertEqual(node_D.parents, [node_N,node_I])
        self.assertEqual(node_D.prob, -1)
        self.assertEqual(node_D.condprob, {
            (True,True):0.3,
            (True, False): 0.6,
            (False, True): 0.95,
            (False, False): 0.05
        })

        nodes_dict["D"] = node_D

        lines = [
            "utility | D",
            "100 +",
            "-10 -"
        ]
        utility_node = UtilityNode.constructUtilityNode(lines,nodes_dict)
        self.assertEqual(utility_node.node_name, "utility")
        self.assertEqual(utility_node.parents, [node_D])
        self.assertEqual(utility_node.condUtility, {
            (True,):100.0,
            (False,):-10.0
        })

if __name__ == '__main__':
    unittest.main()