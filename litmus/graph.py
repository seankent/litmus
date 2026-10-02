###########
# imports #
###########
import copy

#########
# Graph #
#########
class Graph:
    ############
    # __init__ #
    ############
    def __init__(self):
        """
        Constructs an empty directed graph.
        """
        self.adj = {}
        self.adj_t = {}

    ############
    # __repr__ #
    ############
    def __repr__(self):
        """
        Returns the size, e.g. <Graph: 3 vertices, 2 edges>.

        Returns:
            str: The vertex and edge counts.
        """
        edges = 0

        for u in self.adj:
            edges += len(self.adj[u])

        return f"<Graph: {len(self.adj)} vertices, {edges} edges>"

    ###########
    # __str__ #
    ###########
    def __str__(self):
        """
        Returns the adjacency map.

        Returns:
            str: Each vertex mapped to its successors.
        """
        return f"{self.adj}"

    ############
    # __len__ #
    ############
    def __len__(self):
        """
        Returns the number of vertices.

        Returns:
            int: The number of vertices.
        """
        return len(self.adj)

    ################
    # __contains__ #
    ################
    def __contains__(self, u):
        """
        Returns True if the vertex is in the graph.

        Args:
            u (hashable): The vertex to look for.

        Returns:
            bool: True if the vertex is in the graph.
        """
        if u in self.adj:
            return True
        else:
            return False

    ##############
    # add_vertex #
    ##############
    def add_vertex(self, u):
        """
        Adds a vertex, leaving it alone if already present.

        Args:
            u (hashable): The vertex to add.
        """
        if u not in self.adj:
            self.adj[u] = set()
            self.adj_t[u] = set()

    #################
    # remove_vertex #
    #################
    def remove_vertex(self, u):
        """
        Removes a vertex and every edge touching it, ignoring it if absent.

        Args:
            u (hashable): The vertex to remove.
        """
        if u not in self.adj:
            return

        for v in self.adj[u]:
            self.adj_t[v].discard(u)

        for v in self.adj_t[u]:
            self.adj[v].discard(u)

        self.adj.pop(u)
        self.adj_t.pop(u)

    ############
    # add_edge #
    ############
    def add_edge(self, u, v):
        """
        Adds a directed edge from one vertex to another.

        Args:
            u (hashable): The source vertex, which must be in the graph.
            v (hashable): The target vertex, which must be in the graph.
        """
        if u not in self.adj:
            raise KeyError(f"Vertex '{u}' not in graph.")
        if v not in self.adj:
            raise KeyError(f"Vertex '{v}' not in graph.")

        self.adj[u].add(v)
        self.adj_t[v].add(u)

    ###############
    # remove_edge #
    ###############
    def remove_edge(self, u, v):
        """
        Removes a directed edge, ignoring it if absent.

        Args:
            u (hashable): The source vertex, which must be in the graph.
            v (hashable): The target vertex, which must be in the graph.
        """
        if u not in self.adj:
            raise KeyError(f"Vertex '{u}' not in graph.")
        if v not in self.adj:
            raise KeyError(f"Vertex '{v}' not in graph.")

        self.adj[u].discard(v)
        self.adj_t[v].discard(u)

    ############
    # indegree #
    ############
    def indegree(self, u):
        """
        Returns the number of incoming edges.

        Args:
            u (hashable): The vertex to count.

        Returns:
            int: The number of incoming edges.
        """
        return len(self.adj_t[u])

    #############
    # outdegree #
    #############
    def outdegree(self, u):
        """
        Returns the number of outgoing edges.

        Args:
            u (hashable): The vertex to count.

        Returns:
            int: The number of outgoing edges.
        """
        return len(self.adj[u])

    ###########
    # is_sink #
    ###########
    def is_sink(self, u):
        """
        Returns True if the vertex has no outgoing edges.

        Args:
            u (hashable): The vertex to test.

        Returns:
            bool: True if the vertex has no outgoing edges.
        """
        if self.outdegree(u) == 0:
            return True
        else:
            return False

    #############
    # is_source #
    #############
    def is_source(self, u):
        """
        Returns True if the vertex has no incoming edges.

        Args:
            u (hashable): The vertex to test.

        Returns:
            bool: True if the vertex has no incoming edges.
        """
        if self.indegree(u) == 0:
            return True
        else:
            return False

    ############
    # vertices #
    ############
    def vertices(self):
        """
        Returns every vertex in the graph.

        Returns:
            set: Every vertex in the graph.
        """
        return set(self.adj)

    #########
    # sinks #
    #########
    def sinks(self):
        """
        Returns every vertex with no outgoing edges.

        Returns:
            set: Every vertex with no outgoing edges.
        """
        return {u for u in self.adj if self.is_sink(u)}

    ###########
    # sources #
    ###########
    def sources(self):
        """
        Returns every vertex with no incoming edges.

        Returns:
            set: Every vertex with no incoming edges.
        """
        return {u for u in self.adj if self.is_source(u)}

    #########
    # empty #
    #########
    def empty(self):
        """
        Returns True if the graph has no vertices.

        Returns:
            bool: True if the graph has no vertices.
        """
        if self.adj == {}:
            return True
        else:
            return False

    #############
    # reachable #
    #############
    def reachable(self, u, depth = None, visited = None):
        """
        Returns every vertex reachable by following edges forward.

        Args:
            u (hashable): The vertex to walk from.
            depth (int): How many edges to follow, or None to follow all of them.
            visited (set): Vertices already seen, carried through the recursion.

        Returns:
            set: Every vertex reachable from u, which excludes u itself unless it
                sits on a cycle.
        """
        if visited is None:
            visited = set()

        if u not in self.adj:
            return visited

        for v in self.adj[u]:
            if v not in visited:
                visited.add(v)

                if depth is None:
                    self.reachable(v, depth = None, visited = visited)
                elif depth > 0:
                    self.reachable(v, depth = depth - 1, visited = visited)

        return visited

    ########
    # copy #
    ########
    def copy(self):
        """
        Returns a deep copy of the graph.

        Returns:
            Graph: A deep copy of the graph.
        """
        return copy.deepcopy(self)
