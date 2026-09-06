###########
# imports #
###########
from litmus.graph import Graph
from litmus.transaction import Delay

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

        Transactions are vertices and edges are ordering constraints, pointing
        forward in time: an edge from u to v means v cannot fire until u has
        retired. A transaction with no incoming edges has nothing left to wait
        for, which is what ready() returns.

        Anything left unordered runs in parallel. This is a partial order, not a
        sequence.

        The registry holds one entry per interface, tracking the first and last
        transactions appended to it.
        """
        self.graph = Graph()
        self.registry = {}

    ############
    # register #
    ############
    def register(self, itf):
        """
        Declares an interface.

        An interface chains its transactions automatically: each append waits on
        the previous one, so transactions on the same interface never overlap.
        That is the whole point of an interface -- a set of signals can only carry
        one transaction at a time.

        Things that are not driven onto signals, and so do not chain, belong to no
        interface at all. Delay is the one such type today.

        Args:
            itf (str): Interface name.

        Raises:
            KeyError: If the interface is already registered.
        """
        if itf in self.registry:
            raise KeyError(f"Interface '{itf}' already registered.")

        self.registry[itf] = {"first": None, "last": None}

    ##########
    # append #
    ##########
    def append(self, u):
        """
        Appends a transaction to its interface.

        This is the only way a transaction enters the graph. It is placed after
        that interface's previous transaction, so appending is all that is needed
        to sequence an interface. If the previous one has already retired, no edge
        is added, since there is nothing left to wait for.

        A Delay belongs to no interface, so it is added with no ordering of its
        own and any number can be counting down at once. Its ordering comes
        entirely from before() and chain().

        A transaction can only be appended once. Appending one that is already in
        the graph would chain it after itself, so it is rejected rather than
        allowed to build a cycle.

        Args:
            u (Transaction): Transaction to append.

        Raises:
            KeyError: If the transaction's interface is not registered.
            ValueError: If the transaction is already in the graph.
        """
        if u in self.graph:
            raise ValueError(f"Transaction {u} is already in the graph.")

        if isinstance(u, Delay):
            self.graph.add_vertex(u)
            return

        if u.itf not in self.registry:
            raise KeyError(f"Interface '{u.itf}' not registered.")

        self.graph.add_vertex(u)

        if self.registry[u.itf]["first"] is None:
            self.registry[u.itf]["first"] = u

        if self.registry[u.itf]["last"] is not None:
            if self.registry[u.itf]["last"] in self.graph:
                self.graph.add_edge(self.registry[u.itf]["last"], u)

        self.registry[u.itf]["last"] = u

    ##########
    # retire #
    ##########
    def retire(self, u):
        """
        Retires a fired transaction, unblocking whatever waited on it.

        Only a ready transaction can be retired. Dropping one that still has
        dependencies would strand its dependents: they would lose the edge that
        was holding them back and become ready early, silently violating the
        ordering that was asked for. Cancelling a transaction mid-graph is a
        different operation, and would have to reconnect around it.

        Args:
            u (Transaction): Transaction to retire.

        Raises:
            ValueError: If the transaction is not ready.
        """
        if self.graph.indegree(u) != 0:
            raise ValueError(f"Transaction {u} is not ready, it still has dependencies.")

        self.graph.remove_vertex(u)

    ##########
    # before #
    ##########
    def before(self, us, vs):
        """
        Orders everything in vs after everything in us.

        Either side takes a single transaction or a list of them, so the same call
        expresses a one-to-one ordering and a group barrier:

            g.before(a, b)                one to one
            g.before([a, b], c)           c waits on both
            g.before(writes, reads)       no read starts until every write retires

        Every transaction must already be in the graph, so this only adds
        constraints and never appends anything. Keeping insertion on one path means
        a transaction cannot end up on an interface without being chained into
        it.

        The arguments read in time order: us happens first.

        Args:
            us (Transaction or list[Transaction]): Must retire first.
            vs (Transaction or list[Transaction]): Follows.

        Contradictory orderings are not caught here. Checking each edge as it is
        added costs a full traversal per edge, which a barrier between two large
        groups pays for once per pair. validate() catches them in a single pass
        instead.

        Raises:
            KeyError: If any transaction is not in the graph.
        """
        if not isinstance(us, (list, tuple, set)):
            us = [us]

        if not isinstance(vs, (list, tuple, set)):
            vs = [vs]

        for u in us:
            if u not in self.graph:
                raise KeyError(f"Transaction {u} not in graph, append it first.")

        for v in vs:
            if v not in self.graph:
                raise KeyError(f"Transaction {v} not in graph, append it first.")

        for u in us:
            for v in vs:
                self.graph.add_edge(u, v)

    #########
    # chain #
    #########
    def chain(self, us):
        """
        Appends transactions and orders them one after another.

        Each transaction is appended, then ordered after the one before it in the
        list. Use it for a sequence that crosses interfaces, such as a drive
        interleaved with delays; a sequence on a single interface needs nothing
        beyond repeated append().

        Args:
            us (list[Transaction]): Transactions to run in sequence.
        """
        for u in us:
            self.append(u)

        for i in range(1, len(us)):
            self.before(us[i - 1], us[i])

    #########
    # first #
    #########
    def first(self, itf):
        """
        Returns the first transaction appended to an interface.

        This is fixed once set, so it keeps pointing at the same transaction as
        the run progresses, whether or not that transaction has retired.

        Args:
            itf (str): Interface name.

        Returns:
            Transaction: The first transaction appended, or None if nothing has
                been appended to the interface.

        Raises:
            KeyError: If the interface is not registered.
        """
        if itf not in self.registry:
            raise KeyError(f"Interface '{itf}' not registered.")

        return self.registry[itf]["first"]

    ########
    # last #
    ########
    def last(self, itf):
        """
        Returns the most recently appended transaction on an interface.

        Args:
            itf (str): Interface name.

        Returns:
            Transaction: The last transaction appended, or None if nothing has
                been appended to the interface.

        Raises:
            KeyError: If the interface is not registered.
        """
        if itf not in self.registry:
            raise KeyError(f"Interface '{itf}' not registered.")

        return self.registry[itf]["last"]

    #########
    # ready #
    #########
    def ready(self):
        """
        Returns the transactions with nothing left to wait for.

        A transaction is ready once every transaction it depends on has
        retired, which leaves it with no incoming edges. More than one can be
        ready at a time, on different interfaces or among delays.

        Returns:
            set: The ready transactions.
        """
        return self.graph.sources()

    ############
    # validate #
    ############
    def validate(self):
        """
        Checks that the graph can actually run to completion.

        A cycle leaves every transaction on it waiting for itself, so nothing on
        it ever becomes ready and the run hangs rather than failing. The engines
        call this before starting, so a contradictory ordering is reported before
        any simulation time is spent, whether or not the test asked for it.

        A transaction is on a cycle exactly when it can reach itself. That costs a
        traversal per transaction, which is why the check lives here and runs once
        rather than on every before().

        Raises:
            ValueError: If any transaction is on a cycle.
        """
        for u in self.graph.vertices():
            if u in self.graph.reachable(u):
                raise ValueError(f"Transaction {u} is on a cycle, the ordering can never complete.")

    #########
    # empty #
    #########
    def empty(self):
        """
        Returns True once every transaction has retired.
        """
        return self.graph.empty()
