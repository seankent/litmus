###########
# imports #
###########
from litmus.directed_acyclic_graph import DirectedAcyclicGraph

####################
# TransactionGraph #
####################
class TransactionGraph:

    ############
    # __init__ #
    ############
    def __init__(self):
        """
        """
        self.graph = DirectedAcyclicGraph()

    #######
    # add #
    #######
    def add(self, us):
        """
        """
        for u in us:
            if u not in self.graph:
                self.graph.add_vertex(u)

    ########
    # then #
    ########
    def then(self, us, vs):
        """
        """
        if not isinstance(us, (list, tuple, set)):
            us = [us]

        if not isinstance(vs, (list, tuple, set)):
            vs = [vs]

        self.add(us)
        self.add(vs)

        for u in us:
            for v in vs:
                self.graph.add_edge(u, v)

    #########
    # chain #
    #########
    def chain(self, us):
        """
        """
        for i in range(1, len(us)):
            self.then(us[i - 1], us[i])

    #########
    # empty #
    #########
    def empty(self):
        """
        """
        return self.graph.empty()

    ################
    # transactions #
    ################
    def transactions(self, name):
        """
        """
        us = []

        for u in self.graph.vertices():
            if u.name == name:
                us.append(u)
            
        return us


    ########
    # head #
    ########
    def head(self, name):
        """
        """
        candidates = set(self.transactions(name))

        for u in list(candidates):
            if u not in candidates:
                continue

            for v in self.graph.descendants(u):
                if v.name == name:
                    candidates.discard(v)

        return list(candidates)

    ########
    # tail #
    ########
    def tail(self, name):
        """
        """
        candidates = set(self.transactions(name))

        for u in list(candidates):
            if u not in candidates:
                continue

            for v in self.graph.ancestors(u):
                if v.name == name:
                    candidates.discard(v)

        return list(candidates)

    #########
    # ready #
    #########
    def ready(self, name):
        """
        """
        us = []

        for u in self.graph.sources():
            if u.name == name:
                us.append(u)

        return us

    ##########
    # retire #
    ##########
    def retire(self, u):
        """
        """
        if self.graph.indegree(u) != 0:
            raise ValueError(f"Transaction {u} is not ready, it still has dependencies.")

        self.graph.remove_vertex(u)


