
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

        Edges are stored twice. `adj` maps each vertex to the vertices it points
        at, and `adj_t` is its transpose, mapping each vertex to the vertices that
        point at it. Holding both turns indegree into a lookup instead of a scan,
        at the cost of two updates per edge. Every write goes through add_vertex,
        add_edge and remove_edge, so the two can only fall out of step through a
        bug in this class.

        Vertices are dict keys, so any hashable object can be one, and two vertices
        are the same vertex when they compare equal. A vertex type that uses value
        equality will therefore have duplicates silently collapse into a single
        node; types whose duplicates must stay distinct have to keep Python's
        default identity equality.
        """
        self.adj = {}
        self.adj_t = {}

    ############
    # __repr__ #
    ############
    def __repr__(self):
        """
        Returns an unambiguous representation, e.g. <Graph: 3 vertices, 2 edges>.

        This does not round-trip. A graph is built up with add_vertex and add_edge
        rather than constructed from its contents, so there is no expression to
        show. Use str() to see the edges themselves.
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
        Returns the adjacency dict as a string.

        Only the forward direction is shown, since the transpose holds the same
        edges the other way round.
        """
        return f"{self.adj}"

    ############
    # __len__ #
    ############
    def __len__(self):
        """
        Returns the number of vertices.
        """
        return len(self.adj)

    ################
    # __contains__ #
    ################
    def __contains__(self, u):
        """
        Returns True if u is a vertex in the graph.

        Args:
            u: Vertex to check.

        Returns:
            bool: True if u is in the graph.
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
        Adds a vertex, if it is not already present.

        Adding a vertex that already exists is a no-op and leaves its edges intact.

        Args:
            u: Vertex to add.
        """
        if u not in self.adj:
            self.adj[u] = set()
            self.adj_t[u] = set()

    #################
    # remove_vertex #
    #################
    def remove_vertex(self, u):
        """
        Removes a vertex and every edge touching it.

        Removing a vertex that is not in the graph is a no-op. The transpose gives
        the vertices pointing at u directly, so this costs O(degree) rather than a
        scan of the whole graph.

        Args:
            u: Vertex to remove.
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
        Adds a directed edge from u to v.

        Both vertices must already exist. Adding an edge does not create them, so
        that a typo becomes an error rather than a stray vertex.

        Args:
            u: Source vertex.
            v: Destination vertex.

        Raises:
            KeyError: If either vertex is not in the graph.
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
        Removes the directed edge from u to v.

        Removing an edge that is not there is a no-op, but both vertices must
        exist, as for add_edge.

        Args:
            u: Source vertex.
            v: Destination vertex.

        Raises:
            KeyError: If either vertex is not in the graph.
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
        Returns the number of edges arriving at u.

        Args:
            u: Vertex to query.

        Returns:
            int: Number of incoming edges.
        """
        return len(self.adj_t[u])

    #############
    # outdegree #
    #############
    def outdegree(self, u):
        """
        Returns the number of edges leaving u.

        Args:
            u: Vertex to query.

        Returns:
            int: Number of outgoing edges.
        """
        return len(self.adj[u])

    ###########
    # is_sink #
    ###########
    def is_sink(self, u):
        """
        Returns True if no edges leave u.

        Args:
            u: Vertex to query.

        Returns:
            bool: True if u is a sink.
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
        Returns True if no edges arrive at u.

        Args:
            u: Vertex to query.

        Returns:
            bool: True if u is a source.
        """
        if self.indegree(u) == 0:
            return True
        else:
            return False

    #########
    # sinks #
    #########
    def sinks(self):
        """
        Returns every vertex with no outgoing edges.

        Returns:
            set: The sink vertices.
        """
        return {u for u in self.adj if self.is_sink(u)}

    ###########
    # sources #
    ###########
    def sources(self):
        """
        Returns every vertex with no incoming edges.

        Returns:
            set: The source vertices.
        """
        return {u for u in self.adj if self.is_source(u)}

    #########
    # empty #
    #########
    def empty(self):
        """
        Returns True if the graph has no vertices.
        """
        if self.adj == {}:
            return True
        else:
            return False
