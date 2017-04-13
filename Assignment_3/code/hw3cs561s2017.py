from __future__ import division
import copy

class Node:
    def __init__(self,node_name,parents=[],prob=-1,condprob={},is_decision_node=False):
        self.node_name = node_name
        self.parents = parents # type:List[Node]
        self.prob = prob
        self.condprob = condprob # type: dict[(bool,bool),float]
        self.is_decision_node = is_decision_node

    def isDecisionNode(self):
        return self.is_decision_node

    @staticmethod
    def constructNode(lines,nodes_dict):
        lines = [l.strip() for l in lines]
        if lines[1] == "decision":
            return Node(lines[0],is_decision_node=True)
        if len(lines) == 2:
            return Node(lines[0],prob=float(lines[1]))
        node_names = lines[0].replace("|","").split(" ")
        node_names = [n for n in node_names if len(n) > 0]
        node_name = node_names[0]
        parent_nodenames = node_names[1:]
        condprob = {}
        for line in lines[1:]:
            symbols = line.split(" ")[1:]
            prob = float(line.split(" ")[0])
            key = tuple([Utility.convertToBoolean(s) for s in symbols])
            condprob[key] = prob
        parents = [nodes_dict[p] for p in parent_nodenames]
        return Node(node_name,parents=parents,condprob=condprob)

class UtilityNode:
    def __init__(self, node_name, parents, condUtility):
        self.node_name = node_name
        self.parents = parents  # type:List[Node]
        self.condUtility = condUtility # type: dict[(bool,bool),float]

    @staticmethod
    def constructUtilityNode(lines,nodes_dict):
        lines = [l.strip() for l in lines]
        node_names = lines[0].replace("|", "").split(" ")
        node_names = [n for n in node_names if len(n) > 0]
        node_name = node_names[0]
        parent_nodenames = node_names[1:]
        condUtility = {}
        for line in lines[1:]:
            symbols = line.split(" ")[1:]
            prob = float(line.split(" ")[0])
            key = tuple([Utility.convertToBoolean(s) for s in symbols])
            condUtility[key] = prob
        parents = [nodes_dict[p] for p in parent_nodenames]
        return UtilityNode(node_name, parents=parents, condUtility=condUtility)

class BayesNet:
    def __init__(self,node_list,utility_node = None):
        self.nodes = {} # type: dict[str,Node]
        for n in node_list: # type:Node
            self.nodes[n.node_name] = n

        self.utility_node = utility_node
        self.marginalize_cache = {}

    def queryGiven(self,rv_name,evidents):
        """

        :type evidents: dict[str,bool]
        """
        rv_node = self.nodes[rv_name]
        if rv_node.prob != -1:
            prob = rv_node.prob if evidents[rv_name] else 1 - rv_node.prob

        else:
            parents = tuple(evidents[p.node_name] for p in rv_node.parents)
            prob = rv_node.condprob[parents] if evidents[rv_name] else 1 - rv_node.condprob[parents]

        return prob

    def sortTopology(self):
        """
        :rtype: [str]
        """
        variables = list(self.nodes.keys())
        variables.sort()
        s = set()
        l = []
        while len(s) < len(variables):
            for v in variables:
                if v not in s and all(x.node_name in s for x in self.nodes[v].parents):
                    s.add(v)
                    l.append(v)

        return l

    def enumerateAllVariables(self,variables,evidents):
        if len(variables) == 0:
            return 1.0

        v = variables[0]
        if v in evidents:
            result = self.queryGiven(v,evidents) * self.enumerateAllVariables(variables[1:],evidents)
        else:
            immediate_and_all_lower_parents = self.getAllParents(variables)
            depended_upper_parents = immediate_and_all_lower_parents.intersection(set([e for e in evidents.keys()]))
            depended_upper_parents = sorted(list(depended_upper_parents))

            key = v + "|" + ",".join([e + ":" + str(evidents[e]) for e in depended_upper_parents])
            if key in self.marginalize_cache:
                result = self.marginalize_cache[key]
            else:
                probs = []
                evidents_copy = copy.deepcopy(evidents)
                for outcome in [True, False]:
                    evidents_copy[v] = outcome
                    probs.append(
                        self.queryGiven(v, evidents_copy) * self.enumerateAllVariables(variables[1:], evidents_copy))
                result = sum(probs)
                self.marginalize_cache[key] = result

        return result

    def getImmediateParents(self,variable):
        return [p.node_name for p in self.nodes[variable].parents]

    def getAllParents(self,variables):
        s = set()
        for v in variables:
            for p in self.nodes[v].parents:
                s.add(p.node_name)
        return s

    def normalize(self,probs):
        sum_prob_rec = 1.0/sum(probs)
        return [p*sum_prob_rec for p in probs]

    def enumerateProbs(self,variables,evidents):
        node_names_sorted = self.sortTopology()
        variables = [v for v in variables if v not in evidents]

        result = self._enumerateProbs(variables,evidents,node_names_sorted)

        evident_list = [e[0] for e in result]
        prob_list = [e[1] for e in result]
        prob_list = self.normalize(prob_list)
        return zip(evident_list,prob_list)

    def _enumerateProbs(self, variables, evidents,node_names_sorted):
        if len(variables) == 0:
            self.marginalize_cache = {}
            return [(evidents,self.enumerateAllVariables(node_names_sorted,evidents))]

        v = variables[0]
        result = []
        for outcome in [True,False]:
            evidents_copy = copy.deepcopy(evidents)
            evidents_copy[v] = outcome
            result += self._enumerateProbs(variables[1:],evidents_copy,node_names_sorted)

        return result

    def adjustDecisionNodes(self,evidents):
        """
        :type evidents: dict[str,bool]
        """
        for node in self.nodes.values():
            if node.isDecisionNode():
                node.prob = 0.5

        for node_name in evidents:
            decision = evidents[node_name]
            if self.nodes[node_name].isDecisionNode():
                if decision:
                    self.nodes[node_name].prob = 1.0
                else:
                    self.nodes[node_name].prob = 0.0

    def queryProb(self, ask_variables, evidents):
        """
        :type ask_variables: dict[str,bool]
        :type evidents: dict[str,bool]
        """
        self.adjustDecisionNodes(evidents)
        variables = ask_variables.keys()
        result = self.enumerateProbs(variables,evidents)
        for r in result:
            is_violate = False
            assign_values = r[0]
            for v in ask_variables:
                if ask_variables[v] != assign_values[v]:
                    is_violate = True
                    break
            if is_violate:
                continue
            else:
                return r[1]

        return 0.00

    def getExpectedUtility(self,evidents):
        self.adjustDecisionNodes(evidents)
        parents = self.utility_node.parents
        variables = [n.node_name for n in parents]
        result = self.enumerateProbs(variables, evidents)
        expected_value = 0
        for r in result:
            assignment = r[0]
            prob = r[1]
            condition_key = tuple([assignment[v] for v in variables])
            utility_value = self.utility_node.condUtility[condition_key]
            expected_value += utility_value*prob

        return expected_value

    def getMaximumExpectedUtility(self,decision_nodes,evidents):

        result = self._getMaximumExpectedUtility(decision_nodes,evidents)
        key = tuple([result[0][d] for d in decision_nodes])
        return (key,result[1])

    def _getMaximumExpectedUtility(self, decision_nodes, evidents):
        if len(decision_nodes) == 0:
            return (evidents,self.getExpectedUtility(evidents))

        else:
            decision_node = decision_nodes[0]
            evidents_copy = copy.deepcopy(evidents)
            evidents_copy[decision_node] = True
            r1 = self._getMaximumExpectedUtility(decision_nodes[1:],evidents_copy)
            evidents_copy = copy.deepcopy(evidents)
            evidents_copy[decision_node] = False
            r2 = self._getMaximumExpectedUtility(decision_nodes[1:], evidents_copy)
            if r1[1] > r2[1]:
                return r1
            return r2

class Query:
    P_Query = "P"
    EU_Query = "EU"
    MEU_Query = "MEU"
    def __init__(self,query_type,ask_variables={},evidents={},decision_nodes=[]):
        self.query_type = query_type
        self.ask_variables = ask_variables
        self.evidents = evidents
        self.decision_nodes = decision_nodes

    def isPQuery(self):
        return self.query_type == Query.P_Query

    def isEUQuery(self):
        return self.query_type == Query.EU_Query

    def isMEUQuery(self):
        return self.query_type == Query.MEU_Query

    @staticmethod
    def constructQuery(line):
        """
        :type line:str
        :rtype: Node
        """
        line = line.replace(" ","")
        query_type = line.split("(")[0]
        line = line[line.find("(")+1:line.find(")")]

        evidents = {}
        if len(line.split("|")) > 1:
            evident_line = line.split("|")[1]
            for e in evident_line.split(","):
                node_name = e.split("=")[0]
                node_outcome = Utility.convertToBoolean( e.split("=")[1])
                evidents[node_name] = node_outcome

        query_line = line.split("|")[0] #type: str
        decision_nodes = []
        ask_variables = {}
        if query_type == Query.MEU_Query:
            decision_nodes = query_line.split(",")
        else:
            for q in query_line.split(","):
                node_name = q.split("=")[0]
                node_outcome = Utility.convertToBoolean(q.split("=")[1])
                if query_type == Query.EU_Query:
                    evidents[node_name] = node_outcome
                else:
                    ask_variables[node_name] = node_outcome
        if query_type == Query.P_Query:
            return Query(Query.P_Query,ask_variables=ask_variables,evidents=evidents)
        if query_type == Query.EU_Query:
            return Query(Query.EU_Query,evidents=evidents)
        else:
            return Query(Query.MEU_Query,decision_nodes=decision_nodes,evidents=evidents)

class Utility:
    @staticmethod
    def convertToBoolean(symbol):
        if symbol == "+":
            return True
        return False

    @staticmethod
    def convertToSymbol(b):
        if b:
            return "+"
        return "-"

if __name__ == '__main__':

    f = open("input.txt", 'r')
    querys = [] #type: list[Query]
    nodes_dict = {}
    counter = 0 #0 -> read query, 1 -> read node, 2 -> read utility node
    lines = []
    for line in f:
        line = line.strip()
        if counter == 0:
            if line == "******":
                counter = 1
                continue
            else:
                querys.append(Query.constructQuery(line))
        elif counter == 1:
            if line == "***":
                node = Node.constructNode(lines,nodes_dict)
                nodes_dict[node.node_name] = node
                lines = []
                continue
            elif line == "******":
                node = Node.constructNode(lines,nodes_dict)
                nodes_dict[node.node_name] = node
                lines = []
                counter = 2
                continue
            else:
                lines.append(line)
        else:
                lines.append(line)

    utility_node = None
    if counter == 1 and len(lines) > 0:
        node = Node.constructNode(lines,nodes_dict)
        nodes_dict[node.node_name] = node
    elif counter == 2:
        utility_node = UtilityNode.constructUtilityNode(lines,nodes_dict)

    bayes_net = BayesNet(nodes_dict.values(),utility_node=utility_node)

    outputs = []
    for q in querys:
        if q.isPQuery():
            r = bayes_net.queryProb(q.ask_variables,q.evidents)
            outputs.append("{0:.2f}".format(round(r,2)))
        elif q.isEUQuery():
            r = bayes_net.getExpectedUtility(q.evidents)
            outputs.append(str(int(round(r))))
        else:
            result = bayes_net.getMaximumExpectedUtility(q.decision_nodes,q.evidents)
            decision = " ".join([Utility.convertToSymbol(t) for t in result[0]])
            r = int(round(result[1]))
            outputs.append(decision + " " + str(r))

    output_file = open("output.txt", 'w')
    output_file.write("\n".join(outputs))
