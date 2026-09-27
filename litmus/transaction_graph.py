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
        Constructs an empty transaction graph.
        """
        self.graph = DirectedAcyclicGraph()

    #######
    # add #
    #######
    def add(self, us):
        """
        Adds transactions, leaving any already present alone.

        Args:
            us (list): The transactions to add.
        """
        for u in us:
            if u not in self.graph:
                self.graph.add_vertex(u)

    ########
    # then #
    ########
    def then(self, us, vs):
        """
        Orders one group of transactions before another, adding any that are missing.

        Args:
            us (Transaction | list): The transactions that must retire first.
            vs (Transaction | list): The transactions that wait on them.
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
        Orders a list of transactions one after another.

        Args:
            us (list): The transactions to order, first to last.
        """
        for i in range(1, len(us)):
            self.then(us[i - 1], us[i])

    #########
    # empty #
    #########
    def empty(self):
        """
        Returns True if no transactions are left.

        Returns:
            bool: True if no transactions are left.
        """
        return self.graph.empty()

    ################
    # transactions #
    ################
    def transactions(self, name):
        """
        Returns every transaction with a given name.

        Args:
            name (str): The worker name to match.

        Returns:
            list: Every transaction with that name.
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
        Returns the earliest transactions with a given name.

        Args:
            name (str): The worker name to match.

        Returns:
            list: The transactions with that name that no other transaction of
                the same name comes before, directly or indirectly.
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
        Returns the latest transactions with a given name.

        Args:
            name (str): The worker name to match.

        Returns:
            list: The transactions with that name that come before no other
                transaction of the same name, directly or indirectly.
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
        Returns the transactions with a given name that have nothing left to wait on.

        Args:
            name (str): The worker name to match.

        Returns:
            list: The transactions with that name and no remaining dependencies,
                in arbitrary order.
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
        Removes a completed transaction, freeing whatever was waiting on it.

        Args:
            u (Transaction): The transaction to remove, which must have no
                remaining dependencies.
        """
        if self.graph.indegree(u) != 0:
            raise ValueError(f"Transaction {u} is not ready, it still has dependencies.")

        self.graph.remove_vertex(u)


